from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from base import mods
from collections import OrderedDict

from .telegramBot import init_bot
import json
from .models import Graphs

TELEGRAM_BOT_STATUS=False

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
            context['voting'] = voting
        except:
            raise Http404

        return context


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

