from django.conf import settings
from django.db.models import query
from voting import models
from store import models as stmodels
from telegram import Update, CallbackQuery, InputMediaPhoto, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , CallbackContext, CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import datetime,logging
from .website_scrapping import get_graphs
from .models import TelegramBot

#configures and activate '@VotitosBot' to receive any messages from users
def init_bot():

    #logging
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #auth token needed
    updater = Updater(settings.TELEGRAM_TOKEN,
                    use_context=True)

    setup_commands(updater) 
    
    #starts the bot
    updater.start_polling()
       
#configures commands and handlers for the bot
def setup_commands(votitos):

    votitos.dispatcher.add_handler(CommandHandler('start', start))
    votitos.dispatcher.add_handler(CommandHandler('results', show_results))
    votitos.dispatcher.add_handler(CommandHandler('details', show_details))
    votitos.dispatcher.add_handler(CommandHandler('auto', change_auto_status))
    votitos.dispatcher.add_handler(CommandHandler('help', help))
    votitos.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    votitos.dispatcher.add_handler(CallbackQueryHandler(results_query_handler, pattern="^[1-9][0-9]*$"))
    votitos.dispatcher.add_handler(CallbackQueryHandler(details_query_handler, pattern="^d[1-9][0-9]*$")) 
    votitos.dispatcher.add_handler(CallbackQueryHandler(auto_query_handler, pattern="(^True$|^False$)"))
        
#gives the user a warming welcome
def start(update, context):
    name=update.message.from_user.first_name
    id=update.message.chat.id
    context.bot.send_message(chat_id=id, text="Hola {}, a las buenas tardes. ¿En qué puedo ayudarte?".format(name))
    TelegramBot.objects.get_or_create(user_id=id)
    help(update)
    
#list of commands available
def help(update):

    update.message.reply_text("""Esta es mi lista de comandos: 
    /start - Inicia la interacción conmigo
    /results - Muestra los resultados de las votaciones cerradas
    /details - Proporciona detalles de todas las votaciones
    /auto - Permite activar o desactivar las notificaciones automáticas para nuevas votaciones
    """)

#replies to invalid command inputs
def unknown_command(update):
    update.message.reply_text("Lo siento, no sé qué es '%s'. Revisa que has escrito bien el comando o bien revisa mi lista de comandos, puedes hacerlo con\n/help" % update.message.text)

#allow to select an closed voting and show its results
def show_results(update, context):
    update.message.reply_text("Aquí tienes la lista de votaciones finalizadas.")
    finished_votings=models.Voting.objects.exclude(start_date__isnull=True).exclude(end_date__isnull=True)
    keyboard_buttons=[]
    for v in finished_votings:
        keyboard_buttons.append([InlineKeyboardButton(text=str(v.name), callback_data=str(v.id))])
    keyboard=InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=update.message.chat.id, text= "Elige por favor:", reply_markup=keyboard)
    
#handler for '/results' command  
def results_query_handler(update, context):
    
    query=update.callback_query
    query.answer("¡A la orden!")
    results_graph(query.data, update.callback_query.message.chat_id, context)

#allow to select an active or closed voting and show its details    
def show_details(update, context):
    update.message.reply_text("Selecciona la votación de la que desea ver sus detalles") 
    votings=models.Voting.objects.exclude(start_date__isnull=True)
    keyboard_buttons=[[InlineKeyboardButton(text=str(v.name), callback_data="d"+str(v.id)) for v in votings]]
    keyboard=InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=update.message.chat.id, text= "Seleccione una por favor:", reply_markup=keyboard)

#handler for '/details' command
def details_query_handler(update, context):

    query=update.callback_query
    query.answer("¡A la orden!")
    vot_id=query.data[1]
    voting=models.Voting.objects.exclude(start_date__isnull=True).get(id=vot_id)
    msg=aux_message_builder(voting)
    context.bot.send_message(chat_id=query.message.chat_id,text=msg, parse_mode="HTML")

#opt-in and opt-out for auto notifications
def change_auto_status(update, context):
    id=update.message.chat.id
    status_user=TelegramBot.objects.get(user_id=id)
    if status_user is True:
        msg="activadas"
        choose_msg="¿Desea desactivarlas?"
    else:
        msg="desativadas"
        choose_msg="¿Desea activarlas?"
    keyboard_buttons=[[InlineKeyboardButton(text="Sí", callback_data="True")], [InlineKeyboardButton(text="No", callback_data="False")]]  #REVISAR CALLBACK DATA
    keyboard=InlineKeyboardMarkup(keyboard_buttons)
    update.message.reply_text("Actualmente las notificaciones automáticas se encuentran {}.".format(msg)) 
    context.bot.send_message(chat_id=id, text=choose_msg, reply_markup=keyboard)

#handler for '/auto' command
def auto_query_handler(update, context):
    query=update.callback_query
    query.answer("¡Listo! He actualizado tus preferencia")
    id=update.callback_query.message.chat_id
    new_status=query.data
    TelegramBot.objects.filter(user_id=id).update(auto_msg=new_status) 

# ===================
#  AUXILIARY METHODS
# ===================

#auxiliary message to print details from votings
def aux_message_builder(voting):
    
    options=list(voting.question.options.values_list('option', flat=True)) 
    tally=stmodels.Vote.objects.filter(voting_id=voting.id).values('voter_id').distinct().count() #gets unique votes for a voting
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

#extract graph's images from website selected voting and send them to the user
def results_graph(id, chat_identifier, context):
    url=settings.VISUALIZER_VIEW+ str(id)
    images=get_graphs(url)
    if images:
        media_group=[InputMediaPhoto(media=i, caption="PUM en la boquita bb") for i in images]
        context.bot.sendMediaGroup(chat_id=chat_identifier, media=media_group)
    else:
        context.bot.send_message(chat_id=chat_identifier,
        text="Upss! Parece que aún no hay ningún gráfico asociado a esta votación.\nInténtalo de nuevo en otro momento.")
           
#sends notifications when a new voting is created
def auto_notifications(voting):
    users_id_enabled=list(TelegramBot.objects.values_list('user_id', flat=True).exclude(auto_msg=False))
    msg=aux_message_builder(voting)
    for id in users_id_enabled:
        Bot(token=settings.TELEGRAM_TOKEN).send_message(chat_id=id, text=msg, parse_mode="HTML")


