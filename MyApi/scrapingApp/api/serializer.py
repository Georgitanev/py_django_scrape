from rest_framework import serializers
# from firstApp.models import CarSpecs
from scrapingApp.models import Parliament1


class ParliamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament1
        fields = ['id',  'date_born', 'name', 'place_born',  #
                  'profession', 'lang', 'party', 'email', 'fb']
        depth = 1

