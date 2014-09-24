from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
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


from django.core.mail import send_mail
from forms import CotactForm
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('e-mail', '120084324@qq.com'),
				['120084324@qq.com'],
			)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm({'subject':'hhh', 'e-mail':'saasf@gasg.com','message':'nicd'})
	return render_to_response('contact_form.html', {'form': form}, context_instance=RequestContext(request))




