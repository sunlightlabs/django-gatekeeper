from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from gatekeeper.models import ModeratedObject
import datetime
import gatekeeper

@staff_member_required
def moderate(request):
    if request.method == 'POST':
        status = 0
        object_ids = request.POST.getlist('objects')
        if "_deny" in request.POST:
            status = -1
        elif "_approve" in request.POST:
            status = 1
        if status and object_ids:
            for obj_id in object_ids:
                if status == 1:
                    ModeratedObject.objects.get(pk=obj_id).approve(request.user)
                elif status == -1:
                    ModeratedObject.objects.get(pk=obj_id).reject(request.user)

    return HttpResponseRedirect(reverse('gatekeeper_moderate_list'))

@staff_member_required
def moderate_list(request, app_label=None, model=None):
    
    flagged_only = int(request.GET.get("flagged_only", 0))
    content_type = request.GET.get("content_type", None)
    if content_type:
        content_type = ContentType.objects.get(pk=content_type)

    pending = ModeratedObject.objects.filter(moderation_status=0)
    if content_type:
        pending = pending.filter(content_type=content_type)

    if flagged_only:
        pending = pending.filter(flagged=True)
        
    cts = [ContentType.objects.get_for_model(model) for model in gatekeeper.registered_models]
        
    data = {
        "content_type": content_type,
        "flagged_only": flagged_only,
        "pending": pending,
        "cts": cts,
    }
    
    return render_to_response('admin/gatekeeper/moderate.html', data)
