from django.db.models import Sum
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters import FilterSet, DateFilter
from django_filters import rest_framework as filters

from .models import PerformanceMetric
from .serializers import PerformanceMetricSerializer

GROUPING_CHOICES = (
    (0, 'date'),
    (1, 'channel'),
    (2, 'country'),
    (3, 'os'),
)

METRICS_CHOICES = (
    (0, 'impressions'),
    (1, 'clicks'),
    (2, 'installs'),
    (3, 'spend'),
    (4, 'revenue'),
)

class PerformanceMetricsFilter(FilterSet):
    date_from = filters.DateFilter('date', label='date from (YYYY-MM-DD)', lookup_expr='gte')
    date_to = filters.DateFilter('date', label='date to (YYYY-MM-DD)', lookup_expr='lte')
    metrics = filters.MultipleChoiceFilter(label='metrics', choices=METRICS_CHOICES, method='filter_metrics')
    group_by = filters.MultipleChoiceFilter(label='group by', choices=GROUPING_CHOICES, method='group_data')

    class Meta:
        model = PerformanceMetric
        fields = (
            'date_from',
            'date_to',
            'group_by',
            'metrics',
        )

    def filter_metrics(self, queryset, name, value):
        if not value:
            return queryset

        # Create list of metrics to include from 'value' argument
        metrics_to_include = []
        for i in value:
            metrics_to_include.append(METRICS_CHOICES[int(i)][-1])

        if hasattr(self, 'columns_to_group'):
            return queryset.values(*self.columns_to_group, *metrics_to_include)
        else:
            return queryset.values(*metrics_to_include)


    def group_data(self, queryset, name, value):
        if not value:
            return queryset

        # Create list of columns to include from 'value' argument
        self.columns_to_group = []
        for i in value:
            self.columns_to_group.append(GROUPING_CHOICES[int(i)][-1])

        grouped_data = queryset.order_by().values(*self.columns_to_group).distinct() \
            .annotate(impressions=Sum('impressions')) \
            .annotate(clicks=Sum('clicks')) \
            .annotate(installs=Sum('installs')) \
            .annotate(spend=Sum('spend')) \
            .annotate(revenue=Sum('revenue'))

        return grouped_data


class PerformanceMetrics(generics.ListAPIView):
    name = 'performance_metrics'
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    filter_class = PerformanceMetricsFilter

    ordering_fields = (
        'date',
        'channel',
        'country',
        'os',
        'impressions',
        'clicks',
        'installs',
        'spend',
        'revenue',
    )


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request):
        return Response({
            'performance-metrics': reverse('performance_metrics', request=request),
        })
