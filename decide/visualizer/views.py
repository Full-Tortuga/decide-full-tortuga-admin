import json
from django.http import response
from django.http.response import FileResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.generic.base import View

from base import mods

import io
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, landscape, portrait
from reportlab.lib.enums import TA_CENTER

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
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
