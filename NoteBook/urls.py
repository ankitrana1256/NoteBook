from django.contrib import admin
from django.urls import path, include
from accounts import views


admin.site.site_header = 'NoteBook Admin'
admin.site.site_title = "NoteBook Admin Panel"
admin.site.index_title = "Welcome to NoteBook's Admin Panel"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
]
