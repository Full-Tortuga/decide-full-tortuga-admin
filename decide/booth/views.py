import json
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from voting.models import BinaryVoting, MultipleVoting, Voting, ScoreVoting
from django.shortcuts import get_object_or_404

# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        context['token'] = ''
        context['user'] = json.dumps({})

        if self.request.user.is_authenticated:
            token = self.request.session['auth-token']
            user = self.request.user
            context['token'] = token
            context['user'] = json.dumps({"id": user.id})

        try:
            voting = get_object_or_404(Voting,id=vid)
            
            context['voting'] = json.dumps(Voting.toJson(voting))
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class BinaryBoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            voting = get_object_or_404(BinaryVoting,pk=voting_id)
            
            context['voting'] = json.dumps(BinaryVoting.toJson(voting))
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class ScoreBoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            voting = get_object_or_404(ScoreVoting,pk=voting_id)
            
            context['voting'] = json.dumps(ScoreVoting.toJson(voting))
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class MultipleBoothView(TemplateView):
    template_name = 'booth/boothM.html'

    def get_context_data(self, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            voting = get_object_or_404(MultipleVoting,pk=voting_id)
            
            context['voting'] = json.dumps(MultipleVoting.toJson(voting))
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context