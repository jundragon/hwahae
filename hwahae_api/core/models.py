from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractItem(TimeStampedModel):

    """ Abstract Item Definition """

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
