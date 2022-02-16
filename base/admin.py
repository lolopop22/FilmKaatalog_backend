from django.contrib import admin
from base.models import Catalog, Film, Director, Producer, Cast

# Register your models here.
admin.site.register(Catalog)
admin.site.register(Film)
admin.site.register(Director)
admin.site.register(Producer)
admin.site.register(Cast)
