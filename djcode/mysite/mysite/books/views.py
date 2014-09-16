from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from mysite.books.models import Book
# Create your views here.

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		#message = 'You searched for: %r' % request.GET['q']
		q = request.GET['q']
		books = Book.objects.filter(title__icontains=q)
		return render_to_response('search_results.html', {'books':books, 'query':q})
	else:
		message = 'You submitted an empty form.'
		return HttpResponse(message)