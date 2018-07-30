import datetime

from django.db import models

from associations.models.association import Association
from authentication.models import User


class Election(models.Model):
    """
        The election class allows to carry a vote. It should always guarantee the anonymity of the voter.
    """

    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    registered_voters = models.ManyToManyField(User)  # People who are allowed to vote
    voters = models.ManyToManyField(User)  # People who have voted already

    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))

    max_choice_number = models.PositiveIntegerField(default=1)


class VoteChoice(models.Model):

    name = models.CharField(max_length=200)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)


class Vote(models.Model):

    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    choices = models.ManyToManyField(VoteChoice)

    def is_valid(self):  # Should always be true
        return len(self.choices.count()) <= self.election.max_choice_number
