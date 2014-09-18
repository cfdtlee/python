from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from mysite.books.models import Book
# Create your views here.

#def search_form(request):
#    return render_to_response('search_form.html')

def search(request):
	errors = []
	if 'q' in request.GET:
		#message = 'You searched for: %r' % request.GET['q']
		q = request.GET['q']
		if not q:
			errors.append('Enter a search term.')
		elif len(q) > 20:
			errors.append('Please enter at most 20 characters.')
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('search_results.html', {'books': books, 'query': q})
	return render_to_response('search_form.html', {'errors': errors})
		#message = 'You submitted an empty form.'
		#return HttpResponse(message)

def contact(request):
	errors = []
	if request.method == 'POST':
		if not request.POST.get('subject', ''):
			errors.append('Enter a subject.')
		if not request.POST.get('message', ''):
			errors.append('Enter a message')
		if request.POST.get('e-mail') and '@' not in request.POST['e-mail']:
			errors.append('Enter a valid e-mail address.')
		if not errors:
			send_mail(
				request.POST['subject'],
				request.POST['message'],
				request.POST.get('e-mail', 'noreply@example.com'),
				['siteowner@example.com'],
			)
			return HttpResponseRedirect('contact/thanks')
	return render_to_response('contact_form.html', {'errors':errors},  context_instance=RequestContext(request))




