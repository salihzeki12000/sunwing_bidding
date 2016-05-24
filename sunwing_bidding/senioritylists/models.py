from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from sunwing_bidding.users.models import User


# Create your models here.
"""
Seniority List Models
"""


def validate_status(value):
    # validates a pilot status as Captain, First Officer or Seasonal
    if value not in ["CA","FO","SE"]:
        raise ValidationError('enter a valid status, e.g CA, FO, SE')


class Pilot(models.Model):
    """ A model describing an individual pilot who may be included in any number of seniority lists for bidding
        One-to-one relationship with website user from sunwing_bidding custom user module
    """
    ecrew_id = models.IntegerField('ecrew ID', primary_key=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.get_full_name()


@python_2_unicode_compatible
class SeniorityList(models.Model):
    """ A model describing an individual instance of the seniority list which can be used to run a bid
    A seniority list has zero to many seniority list entries
    """
    description = models.CharField('description', max_length=100)  # e.g. 'Seniority List v52' or '2015 Summer Bid List'

    def __str__(self):
        return self.description


@python_2_unicode_compatible
class SeniorityListEntry(models.Model):
    """ A model describing an entry in a seniority list, the same pilot can be in multiple
    seniority lists with different status (eg after upgrade) but only once in any seniority list
    """
    seniority_list = models.ForeignKey(SeniorityList, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)  # unique for seniority_list
    master_seniority = models.IntegerField('master seniority')  # unique for seniority_list
    captain_seniority = models.IntegerField('captain seniority')  # unique for seniority_list
    status = models.CharField('status', max_length=2, validators=[validate_status])  # CA(ptain)/FO/SE(asonal)

    def __str__(self):
        return self.pilot.last_name + ", " + self.pilot.first_name
