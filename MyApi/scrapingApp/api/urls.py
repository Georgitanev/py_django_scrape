from django.conf.urls import url

from .views import ParliamentList
from .views import firstFunction

urlpatterns = [
    url("mp:", firstFunction),
    url("list", ParliamentList.as_view()),  # as_view()
]
