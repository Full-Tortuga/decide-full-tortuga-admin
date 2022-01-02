from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.generic.base import View

from base import mods
from collections import OrderedDict

from django.shortcuts import get_object_or_404
from voting.models import BinaryVoting, MultipleVoting, ScoreVoting

import json, csv
from .telegramBot import init_bot
from .models import Graphs

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
            voting = get_object_or_404(BinaryVoting,pk=voting_id)
            context['voting'] = json.dumps(BinaryVoting.toJson(voting))
        except:
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

def initialize(request):
    #call to initalize telegram bot
    global TELEGRAM_BOT_STATUS
    if not TELEGRAM_BOT_STATUS:
        init_bot()
        TELEGRAM_BOT_STATUS=True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def graphs_requests(request, voting_id):
    if request.method == 'POST':
        data=request.POST.getlist('graphs[]')
        if Graphs.objects.filter(voting_id=voting_id).exists():
            Graphs.objects.filter(voting_id=voting_id).update(graphs_url=data)
        else:
            Graphs.objects.create(voting_id=voting_id, graphs_url=data)
        return HttpResponse()
    
    if request.method == 'GET':       
        data=list(Graphs.objects.filter(voting_id=voting_id).values('voting_id', 'graphs_url'))
        return HttpResponse(json.dumps(data), content_type="application/json")