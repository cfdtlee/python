from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from mysite.books.models import Book
# Create your views here.

#def search_form(request):
#    return render_to_response('search_form.html')

def search(request):
	error = False
	if 'q' in request.GET:
		#message = 'You searched for: %r' % request.GET['q']
		q = request.GET['q']
		if not q:
			error = True
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('search_results.html', {'books': books, 'query': q})
	return render_to_response('search_form.html', {'error': error})
		#message = 'You submitted an empty form.'
		#return HttpResponse(message)