from django.contrib import admin
from gatekeeper.models import ModeratedObject

class ModeratedObjectAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'moderation_status',)
    list_editable = ('moderation_status',)
    list_filter = ['moderation_status','flagged','content_type']

    def object_name(self, obj):
        return "%s" % obj

admin.site.register(ModeratedObject, ModeratedObjectAdmin)

if not admin.site.index_template:
    admin.site.index_template = "admin/gatekeeper/index.html"
