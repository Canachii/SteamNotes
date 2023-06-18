from django.contrib import admin
from .models import App, Rank

# Register your models here.
admin.site.register([App, Rank])
