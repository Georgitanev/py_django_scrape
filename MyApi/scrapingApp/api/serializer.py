from rest_framework import serializers
from scrapingApp.models import Parliament1


class ParliamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament1
        fields = ['id',  'date_born', 'name', 'place_born',
                  'profession', 'lang', 'party', 'email', 'fb']
        depth = 1


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parliament1
        fields = ['name']
        depth = 1


