from collections import OrderedDict
from rest_framework import serializers
from rest_framework.fields import SkipField

from .models import PerformanceMetric


class PerformanceMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceMetric
        fields = [
            'date',
            'channel',
            'country',
            'os',
            'impressions',
            'clicks',
            'installs',
            'spend',
            'revenue',
        ]

    # Removes null fields from Django Rest Framework response
    # Source: https://stackoverflow.com/a/28870066
    def to_representation(self, instance):
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                represenation = field.to_representation(attribute)
                if represenation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(represenation, list) and not represenation:
                   # Do not serialize empty lists
                   continue
                ret[field.field_name] = represenation

        return ret
