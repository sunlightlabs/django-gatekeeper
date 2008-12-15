from django.contrib import admin
from gatekeeper.models import ModeratedObject

class ModeratedObjectAdmin(admin.ModelAdmin):
    list_filter = ['status','content_type']

admin.site.register(ModeratedObject, ModeratedObjectAdmin)

if not admin.site.index_template:
    admin.site.index_template = "admin/gatekeeper/index.html"