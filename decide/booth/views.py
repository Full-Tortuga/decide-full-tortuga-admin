import json
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from voting.models import BinaryVoting, Voting
from django.shortcuts import get_object_or_404

# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class BinaryBoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        try:
            voting = get_object_or_404(BinaryVoting,pk=voting_id)
            context['voting'] = json.dumps({"id": voting.id, 
                                                    "name": voting.name, 
                                                    "desc": voting.desc, 
                                                    "question": {"desc": voting.question.desc, 
                                                                "options": [{"number": voting.question.options.all()[0].number,
                                                                            "option": voting.question.options.all()[0].option}, 
                                                                            {"number": voting.question.options.all()[1].number, 
                                                                            "option": voting.question.options.all()[1].option}]},
                                                    "start_date": str(voting.start_date),
                                                    "end_date": str(voting.end_date),
                                                    "pub_key": {"p": str(voting.pub_key.p), 
                                                                "g": str(voting.pub_key.g), 
                                                                "y": str(voting.pub_key.y)}, 
                                                    "auths": [{"name": voting.auths.all()[0].name, 
                                                                "url": voting.auths.all()[0].url, 
                                                                "me": voting.auths.all()[0].me}], 
                                                    "tally": voting.tally, 
                                                    "postproc": voting.postproc})
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context