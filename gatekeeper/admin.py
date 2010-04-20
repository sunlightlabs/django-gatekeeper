from django.contrib import admin
from gatekeeper.models import ModeratedObject

class ModeratedObjectAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'timestamp', 'moderation_status', 'flagged')
    list_editable = ('moderation_status','flagged')
    list_filter = ['moderation_status','flagged','content_type']

    def object_name(self, obj):
        return "%s" % obj

admin.site.register(ModeratedObject, ModeratedObjectAdmin)
