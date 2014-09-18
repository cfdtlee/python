from django.shortcuts import render_to_response #to use render_to_response
#from django.template.loader import get_template #to use get_template()
#from django.template import Template, Context
from django.http import HttpResponse
import datetime

def current_datetime(request):
    current_date = datetime.datetime.now()
    times = [1,2,3]
    return render_to_response('current_datetime.html', locals())
    #return render_to_response('current_datetime.html', {'current_date':now})
    #t = get_template('current_datetime.html')
    ##t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    #html = t.render(Context({'current_date':now}))
    ##html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)

def hours_ahead(request, offset):
	hours_offset = int(offset)
	next_time = datetime.datetime.now() + datetime.timedelta(hours=hours_offset)
	return render_to_response('hours_ahead.html', locals())
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	#return HttpResponse(html)


def display_meta(request):
    values = request.META.items()
    values.sort()
    return render_to_response('meta.html', locals())
