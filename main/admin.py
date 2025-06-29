from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(book_category)

admin.site.register(book)
admin.site.register(audio)


admin.site.register(Comment)
