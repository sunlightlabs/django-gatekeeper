=================
django-gatekeeper
=================

Django application for moderation of model instances.

Provides convenience methods and an admin interface for moderating instances of registered Django models.

django-gatekeeper is a project of Sunlight Labs (c) 2008.
Writen by Jeremy Carbaugh <jcarbaugh@sunlightfoundation.com>

All code is under a BSD-style license, see LICENSE for details.

Homepage: http://pypi.python.org/pypi/django-gatekeeper/

Source: http://github.com/sunlightlabs/django-gatekeeper/


Requirements
============

python >= 2.4

django >= 1.0


Installation
============

To install run

    ``python setup.py install``

which will install the application into python's site-packages directory.


Quick Setup
===========


settings.py
-----------

Add to INSTALLED_APPS:

	``gatekeeper``
	
Be sure to place gatekeeper above any application which contains models that will be moderated.

Add to MIDDLEWARE_CLASSES:

    ``gatekeeper.middleware.GatekeeperMiddleware``

Add to urls.py:

    url(r'^admin/gatekeeper/', include('gatekeeper.urls')),
    
    
Register Models
---------------

    >>> from django.db import models
    >>> import gatekeeper
    >>> class MyModel(models.Model):
    ...     pass
    >>> gatekeeper.register(MyModel)


Admin Moderation Queue
----------------------

Include the following in urls.py BEFORE the default admin:

    ``url(r'^admin/gatekeeper/', include('gatekeeper.urls')),``


Filtering Moderated Models
--------------------------

Four filter methods are provided to filter instances by moderation status.

    >>> gatekeeper.approved(qs_or_obj)     # approved by moderator
    >>> gatekeeper.pending(qs_or_obj)      # pending in moderation queue
    >>> gatekeeper.rejected(qs_or_obj)     # rejected by moderator
    >>> gatekeeper.unmoderated(qs_or_obj)  # instances not managed by gatekeeper
    
The filter methods take take one parameter which may be either an instance of QuerySet or an instance of Model.


QuerySets
.........

When passed an instance of QuerySet, the filter methods return a new QuerySet containing only moderated objects of the specified state.

    >>> qs = MyModel.objects.filter(creator=request.user)
    >>> my_models = gatekeeper.approved(qs)


Model Instances
...............

When passed an instance of Model, the filter methods return the same instance if it is of the specified status or None if the status does not match. Since the filter methods return None when the object state does not match, they can be used in boolean expressions.

    >>> obj = MyModel.objects.get(pk=obj_id)
    >>> if gatekeeper.approved(obj):
    ...     pass


Deletion of Moderated Objects
-----------------------------

When a moderated object instance is deleted, the associated ModeratedObject instance is deleted as well.


Advanced Usage
==============


Auto-Moderation
---------------

It can be hassle to have to manually moderate objects when there is a simple ruleset used to determine how an object will be moderated. In order to use auto-moderation, the following needs to be added to settings.py:

    ``GATEKEEPER_ENABLE_AUTOMODERATION = True``

Gatekeeper provides two methods of auto-moderation. First, if the user that saves a moderated object has permission to moderate that object, it will be automatically approved. This will always happen if GATEKEEPER_ENABLE_AUTOMODERATION is set to true in settings.py. The second form of auto-moderation allows a moderation method to be written. This method should return True to approve, False to reject, or None to pass on for manual moderation. The auto-moderation function is pass as an argument when registering a Model.

    >>> class MyModel(models.Model):
    ...     pass
    >>> def myautomod(obj):
    ...     pass
    >>> gatekeeper.register(MyModel, auto_moderator=myautomod)

If the auto-moderation function returns None or is not specified for a model, the first form of auto-moderation will be attempted.


Default Moderation
------------------

By default, moderated model instances will be marked as pending and placed on the moderation queue when created. This behavior can be overridden by specifying GATEKEEPER_DEFAULT_STATUS in settings.py.

    * 0 - mark objects as pending and place on the moderation queue
    * 1 - mark objects as approved and bypass the moderation queue
    * -1 - mark objects as rejected and bypass the moderation queue


Import Unmoderated Objects
--------------------------

If gatekeeper is added to an existing application, objects already in the database will not be registered with gatekeeper. You can register existing objects with gatekeeper by passing true to the ``import_unmoderated`` parameter of the registration method. The imported objects will be set to the state specified by GATEKEEPER_DEFAULT_STATUS in settings.py or pending if GATEKEEPER_DEFAULT_STATUS is not set. 

    >>> gatekeeper.register(MyModel, import_unmoderated=True)


Moderation Queue Notifications
------------------------------

Gatekeep will send a notification email to a list of recipients when a new object is placed on the moderation queue. Specify GATEKEEPER_MODERATOR_LIST in settings.py to enable notifications.

    ``GATEKEEPER_MODERATOR_LIST = ['moderator@mysite.com','admin@yoursite.com']``


Post-moderation Signal
----------------------

Many applications will want to execute certain tasks once an object is moderated. Gatekeeper provides a signal that is fired when an object is manually or automatically moderated.

    ``gatekeeper.post_moderation``