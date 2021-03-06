""" model parliament1"""
from django.db import models


class Parliament1(models.Model):
    """ model parliament1"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    date_born = models.DateField(blank=True, null=True)  # date
    place_born = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=80, blank=True, null=True)
    lang = models.CharField(max_length=70, blank=True, null=True)
    party = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    fb = models.CharField(max_length=80, blank=True, null=True)  # facebook url
    url = models.TextField(max_length=15, blank=True, null=True)
    pp = models.TextField(max_length=10, blank=True, null=True)  # political party
    dob = models.TextField(max_length=15, blank=True, null=True)  # date of birth

    def __str__(self):
        return self.name

    class Meta:
        """ db_table parliament1"""

        db_table = "Parliament1"
