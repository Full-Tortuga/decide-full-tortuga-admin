import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from .telegramBot import init_bot
from base import mods

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
    
def initialize(request):
    #call to initalize telegram bot
    init_bot()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

