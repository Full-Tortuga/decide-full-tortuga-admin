from django.conf import settings
from django.db.models import Count
from voting import models
from store import models as stmodels
from telegram import InputMediaPhoto, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import os, sys, base64
from .models import TelegramBot, Graphs
from threading import Thread
from selenium import webdriver
from functools import partial
from dotenv import load_dotenv


load_dotenv() #load token for bot

#auth and front-end for '@VotitosBot'
UPDATER = Updater(os.environ['TELEGRAM_TOKEN'],
                use_context=True)

BOT=Bot(token=os.environ['TELEGRAM_TOKEN'])

URL='http://127.0.0.1:8000/visualizer/'

#configures and activate '@VotitosBot' to receive any messages from users
def init_bot():
    
    setup_commands(UPDATER) 
    updates_setting()
    #starts the bot
    UPDATER.start_polling()
       
#configures commands and handlers for the bot
def setup_commands(votitos):

    dp=votitos.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('relaunch', relaunch, Filters.user(user_id=1931864468)))
    dp.add_handler(CommandHandler('stop', stop, Filters.user(user_id=1931864468)))
    dp.add_handler(CommandHandler('results', partial(voting_selection_menu, command_name='results')))
    dp.add_handler(CommandHandler('details', partial(voting_selection_menu, command_name='details')))
    dp.add_handler(CommandHandler('auto', change_auto_status))
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    dp.add_handler(CallbackQueryHandler(voting_selection_query_handler, pattern="^v_[a-zA-Z]+_[a-zA-Z]+$"))
    dp.add_handler(CallbackQueryHandler(results_query_handler, pattern="^[1-9][0-9]*_[a-zA-Z]+$"))
    dp.add_handler(CallbackQueryHandler(details_query_handler, pattern="^d[1-9][0-9]*_[a-zA-Z]+$")) 
    dp.add_handler(CallbackQueryHandler(auto_query_handler, pattern="(^True$|^False$)"))

#set bot configuration not to reply to old messages
def updates_setting():
    updates=BOT.get_updates() 
    if updates:
        last_update=updates[-1].update_id
        BOT.get_updates(offset=last_update+1)  
             
#gives the users a warming welcome
def start(update, context):
    name=update.message.from_user.first_name
    id=update.message.chat.id
    context.bot.send_message(chat_id=id, text="Hola {}, a las buenas tardes. ¿En qué puedo ayudarte?".format(name))
    TelegramBot.objects.get_or_create(user_id=id)
    help(update, context)
    
# relaunch the bot and also the whole project (limited to admin)
def relaunch(update, context):
    Thread(target=stop_restart).start()
    
# aux for relaunch
def stop_restart():
    UPDATER.stop()
    os.execl(sys.executable, sys.executable, *sys.argv) 

#shut down the bot   
def stop(update, context):
    UPDATER.stop()
    
#list of available commands
def help(update, context):

    update.message.reply_text("""Esta es mi lista de comandos: 
    /start - Inicia la interacción conmigo
    /results - Muestra los resultados de las votaciones cerradas
    /details - Proporciona detalles de todas las votaciones
    /auto - Permite activar o desactivar las notificaciones automáticas para nuevas votaciones
    """)

#replies to invalid command inputs
def unknown_command(update, context):
    update.message.reply_text("Lo siento, no sé qué es '%s'. Revisa que has escrito bien el comando o bien revisa mi lista de comandos, puedes hacerlo con\n/help" % update.message.text)

#allows you to select a closed voting and show its results
def show_results(update, context, chat_identifier, vot_type):
    votings=get_voting_objects(vot_type)
    finished_votings=votings.exclude(start_date__isnull=True).exclude(end_date__isnull=True)
    type=vot_type.split("_")[1]
    if finished_votings is not None:
        keyboard_buttons=[]
        for v in finished_votings:
            keyboard_buttons.append(InlineKeyboardButton(text=str(v.name), callback_data=str(v.id)+"_"+type))
        keyboard=InlineKeyboardMarkup(build_keyboard_menu(keyboard_buttons,2))
        context.bot.send_message(chat_id=chat_identifier, text= "Aquí tienes la lista de votaciones finalizadas. Elige por favor:", reply_markup=keyboard)
    else:
        context.bot.send_message(chat_id=chat_identifier, text= "Vaya...no hay ninguna votación de este tipo que haya finalizado.\nInténtalo de nuevo en otro momemnto")
    
#handler for '/results' command  
def results_query_handler(update, context):
    
    query=update.callback_query
    query.answer("¡A la orden!")
    response_array=query.data.split("_")
    results_graph(query.data[0], query.data[1], query.message.chat_id, context)

#allows you to select an active or closed voting and show its details    
def show_details(update, context, chat_identifier,vot_type):
    
    votings=get_voting_objects(vot_type)
    started_votings=votings.exclude(start_date__isnull=True)
    type=vot_type.split("_")[1]
    if started_votings is not None:
        keyboard_buttons=[InlineKeyboardButton(text=str(v.name), callback_data="d"+str(v.id)+"_"+type) for v in started_votings]
        keyboard=InlineKeyboardMarkup(build_keyboard_menu(keyboard_buttons,2))
        context.bot.send_message(chat_id=chat_identifier, text="Selecciona la votación de la que desea ver sus detalles", reply_markup=keyboard)
    else:
        context.bot.send_message(chat_id=chat_identifier, text= "Vaya...no hay ninguna votación de este tipo ahora mismo.\nInténtalo de nuevo en otro momemnto")
        
#handler for '/details' command
def details_query_handler(update, context):
    query=update.callback_query
    query.answer("¡A la orden!")
    response_array=query.data.split("_")
    vot_id=response_array[0][1]
    vot_type=response_array[1]
    
    voting=get_voting_objects(vot_type).exclude(start_date__isnull=True).get(id=vot_id)
    v_type=translate_to_type(vot_type)
    msg=aux_message_builder(voting,v_type)
    context.bot.send_message(chat_id=query.message.chat_id,text=msg, parse_mode="HTML")

#opt-in and opt-out for auto notifications
def change_auto_status(update, context):
    id=update.message.chat.id
    status_user=TelegramBot.objects.get(user_id=id)
    if status_user.auto_msg:
        choose_msg="Actualmente las notificaciones automáticas se encuentran activadas.\n¿Desea desactivarlas?"
        keyboard_buttons=build_keyboard_menu([InlineKeyboardButton(text="Sí", callback_data="False"),
                          InlineKeyboardButton(text="No", callback_data="True")], 2)

    else:
        choose_msg="Actualmente las notificaciones automáticas se encuentran desactivadas.\n¿Desea activarlas?"
        keyboard_buttons=build_keyboard_menu([InlineKeyboardButton(text="Sí", callback_data="True"),
                          InlineKeyboardButton(text="No", callback_data="False")], 2)
    keyboard=InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=id, text=choose_msg, reply_markup=keyboard)

#handler for '/auto' command
def auto_query_handler(update, context):
    query=update.callback_query
    u_id=query.message.chat_id
    msg_id=query.message.message_id
    for id in range(msg_id, msg_id+1):
        context.bot.delete_message(chat_id=u_id, message_id=id)
    TelegramBot.objects.filter(user_id=u_id).update(auto_msg=query.data) 
    query.answer("¡Listo! He actualizado tus preferencias")

        
# =====================
#   AUXILIARY METHODS
# =====================

#auxiliary keyboard to select voting type and get command name
def voting_selection_menu(update, context, command_name):
    keyboard_buttons = [InlineKeyboardButton('Votación simple', callback_data='v_simple_'+command_name),
              InlineKeyboardButton('Votación binaria', callback_data='v_binary_'+command_name),
              InlineKeyboardButton('Votación múltiple', callback_data='v_multiple_'+command_name),
              InlineKeyboardButton('Votación por puntuación', callback_data='v_score_'+command_name)]
    context.bot.send_message(chat_id=update.message.chat.id, text="Elige el tipo de votación:", reply_markup=InlineKeyboardMarkup(build_keyboard_menu(keyboard_buttons,2)))
    
    
#handler for voting selection
def voting_selection_query_handler(update, context):
    query=update.callback_query
    vot_type_command=query.data
    if 'details' in vot_type_command:
        show_details(update, context, query.message.chat_id, vot_type_command)
    elif 'results' in vot_type_command:
        show_results(update, context, query.message.chat_id, vot_type_command)
    query.answer()
  
           
#constructs menu for inline buttons    
def build_keyboard_menu(buttons, n_cols):
    return [buttons[b:(b + n_cols)] for b in range(0, len(buttons), n_cols)]
        
#auxiliary message to print details from votings
def aux_message_builder(voting, vot_type):
    
    options=list(voting.question.options.values_list('option', flat=True))
    if stmodels.Vote.objects.filter(voting_id=voting.id, type=vot_type).exists():
        unique_votes=set(stmodels.Vote.objects.filter(voting_id=voting.id, type=vot_type).annotate(Count('voter_id', distinct=True))
                           .values_list('voter_id'))
        tally=len(unique_votes)
    else:
        tally=0
    start_d=voting.start_date.strftime('%d-%m-%Y %H:%M:%S')+"\n"
    end_d="Por decidir\n"

    if voting.end_date is not None:
        end_d=voting.end_date.strftime('%d-%m-%Y %H:%M:%S')+"\n"
    elif tally is None:
        tally="Desconocido por el momento"
  
    opt_msg=""
    for i,o in enumerate(options,1): 
        opt_msg+="  " + str(i)+". " + o+"\n"
    
    msg="<b>{}\n\n</b><b><i>Descripción:</i></b> {}\n<b><i>Pregunta:</i></b> {}\n".format(str(voting.name).upper(), voting.desc, str(voting.question)) 
    msg+="<b><i>Opciones:</i></b>\n{}\n".format(opt_msg)
    msg+="<b><i>Fecha de incio:</i></b> {}<b><i>Fecha de finalización:</i></b> {}<b><i>Conteo actual:</i></b> {}".format(start_d, end_d, tally)
    
    return msg


#extracts graph's images from website selected voting and sends them to the user
def results_graph(id, vot_type, chat_identifier, context):
    open_graphs_generator_view(id, vot_type)
    if Graphs.objects.filter(voting_id=id).exists():
        graphs_base64=Graphs.objects.filter(voting_id=id).values('graphs_url')
        try:
            base64_url_list=eval(graphs_base64[0]['graphs_url'])
            b64_images=[]
            media_group=[]
            for i in range(0,len(base64_url_list)):
                b64_images.append(base64_url_list[i].split(",")[1])
                path="graph_"+str(id)+"_"+str(i)+".png"
                with open(path,"wb") as f:
                    f.write(base64.b64decode(b64_images[i]))
                media_group.append(InputMediaPhoto(media=open(path, 'rb')))
                os.remove(path)
            context.bot.sendMediaGroup(chat_id=chat_identifier, media=media_group)
        except:
            context.bot.send_message(chat_id=chat_identifier,
            text="Vaya...no hay gráficas disponibles para mostrar.\nInténtalo de nuevo más tarde.")
        
    else:
        context.bot.send_message(chat_id=chat_identifier,
        text="Upss! Parece que aún no hay ninguna gráfica asociada a esta votación.\nInténtalo de nuevo en otro momento.")


#uses selenium to call view which generates voting graphs
def open_graphs_generator_view(id, vot_type):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver=webdriver.Chrome(options=options)
    view_url=translate_to_url(vot_type)
    driver.get(view_url + str(id)) 
    
#sends notifications when a new voting is created
def auto_notifications(voting):
    users_id_enabled=list(TelegramBot.objects.values_list('user_id', flat=True).exclude(auto_msg=False))
    msg=aux_message_builder(voting, voting.type)
    if users_id_enabled:
        for id in users_id_enabled:
            BOT.send_message(chat_id=id, text=msg, parse_mode="HTML")


#gets voting type objects
def get_voting_objects(vot_type):
    res=None
    if 'simple' in vot_type:
       res=models.Voting.objects
    elif 'binary' in vot_type:
        res=models.BinaryVoting.objects
    elif 'multiple' in vot_type:
        res=models.MultipleVoting.objects
    elif 'score' in vot_type:
        res=models.ScoreVoting.objects
    return res

#translate vot_type var to actual voting type name
def translate_to_type(vot_type):
    res=None
    if 'simple' in vot_type:
        res=('V', 'Voting')
    elif 'binary' in vot_type:
        res=('BV', 'BinaryVoting')
    elif 'multiple' in vot_type:
        res=('MV', 'MultipleVoting')
    elif 'score' in vot_type:
        res=('SV', 'ScoreVoting')
    return res  

#translate vot_type var to url of that type
def translate_to_url(vot_type):
    if 'binary' in vot_type:
        res=URL+'binaryVoting/'
    elif 'multiple' in vot_type:
        res=URL+'multipleVoting/'
    elif 'score' in vot_type:
        res=URL+'scoreVoting/'
    else:
        res=URL
    return res