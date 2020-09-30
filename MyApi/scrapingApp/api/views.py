from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .serializer import ParliamentSerializer
from scrapingApp.models import Parliament1
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

@api_view()
@permission_classes([AllowAny])
def firstFunction(request):
    print(request.query_params)
    print(request.query_params['num'])
    number = request.query_params['num']
    new_number = int(number) * 2
    return Response({'message': "we received your request", 'result': new_number})


# class ParliamentViewset(viewsets.ModelViewSet):
#     serializer_class = ParliamentSerializer
#
#     def get_queryset(self):
#         data_all = Parliament1.objects.all()
#         return data_all


class ParliamentList(generics.ListAPIView):
    serializer_class = ParliamentSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Parliament1.objects.all()
    print(filter_backends)
    filterset_fields = ['id', 'date_born', 'name', 'place_born', 'profession', 'lang', 'party', 'email', 'fb']


