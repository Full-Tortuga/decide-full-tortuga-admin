from .models import Graphs
from rest_framework import serializers

class GraphSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Graphs
        fields=['voting_id', 'voting_type', 'graphs_url']