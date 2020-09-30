from django.conf.urls import url, include
from .views import firstFunction  #, deleteObjects

from .views import ParliamentList
from django.urls import re_path

from rest_framework.routers import DefaultRouter

# from .views import ParliamentViewset

# router = DefaultRouter()
# router.register('parliament', ParliamentViewset, basename='Parliament1')


urlpatterns = [
    url('first/', firstFunction),
    url('list', ParliamentList.as_view()),
]

