from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from scrapingApp.models import Parliament1

from .serializer import ParliamentSerializer


@api_view()
@permission_classes([IsAuthenticated])
def firstFunction(request):
    number = request.query_params["id"]
    mp = Parliament1.objects.values(
        "id",
        "date_born",
        "name",
        "place_born",
        "profession",
        "lang",
        "party",
        "email",
        "fb",
        "url",
        "pp",
        "dob",
    ).filter(id=number)
    return Response(mp)


@permission_classes([IsAuthenticated])
class ParliamentList(generics.ListAPIView):
    serializer_class = ParliamentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    queryset = Parliament1.objects.all()
    print(filter_backends)
    filterset_fields = [
        "id",
        "date_born",
        "name",
        "place_born",
        "profession",
        "lang",
        "party",
        "email",
        "fb",
        "pp",
        "dob",
    ]
