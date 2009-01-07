from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime
import gatekeeper

STATUS_CHOICES = (
    (1, "Approved"),
    (0, "Pending"),
    (-1, "Rejected"),
)

class ModeratedObjectManager(models.Manager):
    
    def get_for_instance(obj):
        ct = ContentType.objects.get_for_model(obj.__class__)
        try:
            mo = ModeratedObject.objects.get(content_type=ct, object_id=obj.pk)
            return mo
        except ModeratedObject.DoesNotExist:
            pass
            
class ModeratedObject(models.Model):
    
    objects = ModeratedObjectManager()
    
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    status = models.IntegerField(choices=STATUS_CHOICES)
    moderated_by = models.ForeignKey(User, blank=True, null=True)
    moderation_date = models.DateTimeField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['timestamp']
    
    def __unicode__(self):
        return "[%s] %s" % (self.get_status_display(), self.content_object)
        
    def get_absolute_url(self):
        if hasattr(self.content_object, "get_absolute_url"):
            return self.content_object.get_absolute_url()
        
    def _moderate(self, status, user):
        self.status = status
        self.moderated_by = user
        self.moderation_date = datetime.datetime.now()
        self.save()
        gatekeeper.post_moderation.send(sender=ModeratedObject, instance=self)

    def approve(self, user):
        self._moderate(1, user)

    def reject(self, user):
        self._moderate(-1, user)