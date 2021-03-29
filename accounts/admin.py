from django.contrib import admin
from .models import Subject, Notes, Semester, Unit


# Register your models here.
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Notes)
admin.site.register(Unit)