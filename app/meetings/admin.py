from django.contrib import admin
from .models import Course, Meeting, Review

admin.site.register(Course)
admin.site.register(Meeting)
admin.site.register(Review)