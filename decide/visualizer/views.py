import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
import ast
from base import mods
from collections import OrderedDict
from .telegramBot import init_bot


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
    init_bot()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

