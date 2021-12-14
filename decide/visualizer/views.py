import json
from django.http import response
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.generic.base import View

from base import mods
from collections import OrderedDict

import json



#Generate a CSV File 
class Votes_csv(View):
    def get(self,request,*args,**kwargs):

        return response

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
