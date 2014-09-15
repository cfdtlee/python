from django.contrib import admin
from mysite.books.models import Publisher, Author, Book

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email')
	search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'publisher', 'publication_data')
	list_filter = ('publication_data',)
	date_hierarchy = 'publication_data'
	ordering = ('-publication_data',)
	fields = ('title', 'authors', 'publisher') #the order of editing page
	filter_horizontal = ('authors',) #easier for selection
	raw_id_fields = ('publisher',)

admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
