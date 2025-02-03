from django.contrib import admin
from .models import *
# Register your models here.


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    
class BookInline(admin.TabularInline):
    model = Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN')
    inlines = [BookInstanceInline]
    search_fields = ['title']
  
  

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'due_back', 'status') 
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )
    
    
    
class AuthorAdmin(admin.ModelAdmin):
    # Controls fields to display table wide
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Controls fields to display on the detail views
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)
