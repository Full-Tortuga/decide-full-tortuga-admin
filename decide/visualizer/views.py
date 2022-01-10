import json, ast, requests, csv
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.generic.base import View
from base import mods
from collections import OrderedDict
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import GraphSerializer
from .models import Graphs
from .telegramBot import init_bot
from django.shortcuts import get_object_or_404
from voting.models import BinaryVoting, MultipleVoting, ScoreVoting

TELEGRAM_BOT_STATUS=False

#Generate a CSV File 
class Votes_csv(View):
    def get(self,request,*args,**kwargs):
        vid = kwargs.get('voting_id', 0)
        try:
            r = mods.get('voting', params={'id':vid})
            dataList =eval(r[0]['postproc'])
            voting = []
            for e in dataList:
                voting.append(dict(e))
        except:
            raise Http404

        res = HttpResponse(content_type="text/csv")
        res['Content-Disposition'] = 'attachment; filename=' + str(r[0]["id"]) + '.csv'

        csv_file = csv.writer(res)
        csv_file.writerow(["Opcion", "Puntuacion", "Votos"])
        for vote in voting:
            csv_file.writerow([vote["option"], vote["postproc"], vote["votes"]])
        return res

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        try:
            r = mods.get('voting', params={'id': vid})
            dataList =eval(r[0]['postproc'])
            ls_dicc = []
            for e in dataList:
                ls_dicc.append(dict(e))
            voting = (r[0], ls_dicc)
            context['voting'] = json.dumps(voting)
        except:
            raise Http404

        return context

class VisualizerViewScoring(TemplateView):
    template_name = 'visualizer/visualizer_scoring.html'

    def get_context_data(self,voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            voting = get_object_or_404(ScoreVoting,pk=voting_id)
            context['voting'] = json.dumps(ScoreVoting.toJson(voting))
        except:
            raise Http404

        return context

class VotesScoring_csv(View):
    def get(self,request,voting_id,*args,**kwargs):
        try:
            voting = get_object_or_404(ScoreVoting,pk=voting_id)
        except:
            raise Http404
        res = HttpResponse(content_type="text/csv")
        res['Content-Disposition'] = 'attachment; filename=' + str(voting.id) + '-ScoringVoting.csv'

        csv_file = csv.writer(res)

        csv_file.writerow(["Opcion", "Puntuacion", "Votos"])

        for vote in voting.postproc:
            csv_file.writerow([vote["option"], vote["postproc"], vote["votes"]])
        return res

class VisualizerViewBinary(TemplateView):
    template_name = 'visualizer/visualizer_binary.html'

    def get_context_data(self,voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            print("HOLA TRY")
            voting = get_object_or_404(BinaryVoting,pk=voting_id)
            context['voting'] = json.dumps(BinaryVoting.toJson(voting))
        except:
            print("HOLA CATCH")
            raise Http404

        return context

class VotesBinary_csv(View):
    def get(self,request,voting_id,*args,**kwargs):
        try:
            voting = get_object_or_404(BinaryVoting,pk=voting_id)
        except:
            raise Http404

        res = HttpResponse(content_type="text/csv")
        res['Content-Disposition'] = 'attachment; filename=' + str(voting.id) + '.csv'

        csv_file = csv.writer(res)

        csv_file.writerow(["Opcion", "Puntuacion", "Votos"])

        for vote in voting.postproc:
            csv_file.writerow([vote["option"], vote["postproc"], vote["votes"]])
        return res
        
class VisualizerViewMultiple(TemplateView):
    template_name = 'visualizer/visualizer_multiple.html'

    def get_context_data(self,voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            voting = get_object_or_404(MultipleVoting,pk=voting_id)
            context['voting'] = json.dumps(MultipleVoting.toJson(voting))
        except:
            raise Http404

        return context

class VotesMultiple_csv(View):
    def get(self,request,voting_id,*args,**kwargs):
        try:
            voting = get_object_or_404(MultipleVoting,pk=voting_id)
        except:
            raise Http404

        res = HttpResponse(content_type="text/csv")
        res['Content-Disposition'] = 'attachment; filename=' + str(voting.id) + '.csv'

        csv_file = csv.writer(res)

        csv_file.writerow(["Opcion", "Puntuacion", "Votos"])

        for vote in voting.postproc:
            csv_file.writerow([vote["option"], vote["postproc"], vote["votes"]])
        return res
    
class GraphViewSet(viewsets.ModelViewSet):
		   
	serializer_class=GraphSerializer
	http_method_names = ['get']
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['voting_id', 'voting_type']
	    
	def get_queryset(self):
	    return Graphs.objects.all()

def initialize(request):
    #call to initalize telegram bot
    global TELEGRAM_BOT_STATUS
    if not TELEGRAM_BOT_STATUS:
        try:    #just in case someone from another team tried to start the bot when other team already did
            init_bot()
        except:
            pass
            TELEGRAM_BOT_STATUS=True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       

def graphs_requests(request, voting_id):
    if request.method == 'POST':
        vot_type=request.POST.get('type')
        urls=request.POST.getlist('graphs[]')
        if Graphs.objects.filter(voting_id=voting_id, voting_type=vot_type).exists():
            to_update=Graphs.objects.get(voting_id=voting_id, voting_type=vot_type)
            to_update.voting_type=vot_type
            to_update.graphs_url=urls
            to_update.save()
        else:
            Graphs.objects.create(voting_id=voting_id, voting_type=vot_type, graphs_url=urls)
        return HttpResponse()
    
    if request.method == 'GET':  
        vot_type=translate_type(request.path_info)   
        data=list(Graphs.objects.filter(voting_id=voting_id, voting_type=vot_type).values('voting_id', 'voting_type','graphs_url'))        
        return HttpResponse(json.dumps(data), content_type="application/json")
    
#translate path to vot_type
def translate_type(path_url):
    vot_type='V'
    if 'binaryVoting' in path_url:
        vot_type='BV'
    elif 'multiple' in path_url:
        vot_type='MV'
    elif 'score' in path_url:
        vot_type='SV'
    return vot_type   
