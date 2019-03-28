from django.db import models

CHANNEL_MAX_LENGTH = 40
COUNTRY_MAX_LENGTH = 2
OS_MAX_LENGTH = 7
OS_CHOICES = (
    (1, 'android'),
    (2, 'ios'),
)

class PerformanceMetric(models.Model):

    date = models.DateField(null=True)

    channel = models.CharField(max_length=CHANNEL_MAX_LENGTH, null=True)

    country = models.CharField(max_length=COUNTRY_MAX_LENGTH, null=True)

    os = models.CharField(max_length=OS_MAX_LENGTH, choices=OS_CHOICES, null=True)

    impressions = models.PositiveIntegerField(null=True)

    clicks = models.PositiveIntegerField(null=True)

    installs = models.PositiveIntegerField(null=True)

    spend = models.FloatField(null=True)

    revenue = models.FloatField(null=True)

    class Meta:
        ordering = ('date',)


