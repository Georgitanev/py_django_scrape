from django.conf.urls import url, include
from .views import firstFunction  #, deleteObjects
from rest_framework.routers import DefaultRouter
from .views import ParliamentViewset

router = DefaultRouter()
router.register('parliament', ParliamentViewset, basename='Parliament1')


urlpatterns = [
    url('first', firstFunction),
    url('', include(router.urls))
]

