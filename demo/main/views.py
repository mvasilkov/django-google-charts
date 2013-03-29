from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import Payment
from qsstats import QuerySetStats

def time_series(queryset, date_field, interval, func=None):
    qsstats = QuerySetStats(queryset, date_field, func)
    return qsstats.time_series(*interval)

def home(request):
    series = {'count': [], 'total': []}
    queryset = Payment.objects.all()
    y = 2011
    for m in range(1, 4):
        start = datetime(y, m, 1)
        end = start + relativedelta(months=1)
        series['count'].append(time_series(queryset, 'datetime', [start, end]))
        series['total'].append(time_series(queryset, 'datetime', [start, end], func=Sum('amount')))

    start = datetime(y, 1, 1)
    end = start + relativedelta(months=3)
    series['count_3'] = time_series(queryset, 'datetime', [start, end])
    series['total_3'] = time_series(queryset, 'datetime', [start, end], func=Avg('amount'))

    return render_to_response('home.html', {'series': series},
                              context_instance=RequestContext(request))
