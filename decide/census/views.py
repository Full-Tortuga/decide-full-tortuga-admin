from django.db.utils import Error
from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.status import (
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from django.contrib.auth.models import User


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        type = request.data.get('type')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter, type=type)
                if Census.objects.filter(voting_id=voting_id, voter_id=voter, type=type).exists():
                    return Response('Error try to create census', status=ST_409)
                census.save()
        except ValidationError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        type = request.GET.get('type')
        voters = Census.objects.filter(
            voting_id=voting_id, type=type).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        type = request.data.get('type')
        census = Census.objects.filter(
            voting_id=voting_id, voter_id__in=voters, type=type)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voters = []
        try:
            if voting_id == 0 or voting_id == None:
                census = Census.objects.all()
            else:
                census = Census.objects.filter(voting_id=voting_id)
            for c in census:
                try:
                    user = User.objects.get(id=c.voter_id)
                    voters.append({'id': user.id, 'username': user.username,
                                   'first_name': user.first_name, 'last_name': user.last_name,
                                   'email': user.email, 'gender': c.gender, 'region': c.region,
                                   'voting_id': c.voting_id})
                except User.DoesNotExist:
                    continue
        except Error:
            return Response('Invalid voting', status=ST_400)
        return Response(voters)
