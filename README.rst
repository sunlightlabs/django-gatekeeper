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

``gatekeeper.register`` optionally takes some extra parameters for advanced configuration, see `advanced register options`_ for details.


Admin Moderation Queue
----------------------

Include the following in urls.py BEFORE the default admin:

    ``url(r'^admin/gatekeeper/', include('gatekeeper.urls')),``


Accessing Moderated Models
--------------------------

Models registered with ``gatekeeper.register`` are given a custom manager that adds several extra fields.  (As documented in `advanced register options`_ all of these fields can be renamed via special parameters to ``gatekeeper.register`` but for simplicity they will be referred to by their default names throughout this document.)

Model Instance Convenience Fields
.................................

Every model instance accessed via the custom manager ('objects' by default) has a few extra read-only fields tacked on:

* moderation_status - current moderation status (APPROVED_STATUS, PENDING_STATUS, or REJECTED_STATUS)
* flagged - flag status (True or False)

In addition, ``moderation_object`` is provided as a shortcut to access the actual ``ModeratedObject`` instance.  The first access of this attribute incurs a database hit but the instance is then cached for the object lifetime.

GatekeeperQuerySet
..................

The custom manager returns a special GatekeeperQuerySet with a few extra filters:

    >>> MyModel.objects.all().approved()     # approved by moderator
    >>> MyModel.objects.all().pending()      # pending in moderation queue
    >>> MyModel.objects.all().rejected()     # rejected by moderator
    >>> MyModel.objects.all().flagged()      # flagged 
    >>> MyModel.objects.all().not_flagged()  # not flagged

These are implemented on the `GatekeeperQuerySet` itself so that they can be chained:

    >>> MyModel.objects.filter(spam=eggs).rejected().flagged()


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

    * ``gatekeeper.PENDING_STATUS`` - mark objects as pending and place on the moderation queue
    * ``gatekeeper.APPROVED_STATUS`` - mark objects as approved and bypass the moderation queue
    * ``gatekeeper.PENDING_STATUS`` - mark objects as rejected and bypass the moderation queue

Moderation On Flagging
----------------------

Flagging is provided as a simple mechanism to allow for users to flag content generally for further review.  By default flagging an object does not change it's moderation status, but GATEKEEPER_STATUS_ON_FLAG is available toalter this behavior.  If GATEKEEPER_STATUS_ON_FLAG is set to one of the status constants (see `Default Moderation`_) the given status will be set for an object when ``ModeratedObject.flag`` is called.

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

Advanced Register Options
-------------------------

``gatekeeper.register`` takes a few optional parameters:

manager_name:
    name of manager to add/replace on model (defaults to objects)
status_name:
    name of moderation status field to add to model instances (defaults to ``moderation_status``)
flagged_name:
    name of flagged field to add to model instances (defaults to ``flagged``)
moderation_object_name:
    name of moderation_object accessor to add to model instances (defaults to ``moderation_object``)
base_manager:
    Manager for contributed manager placed at ``manager_name`` to inherit from.  Default behavior is to attempt to inherit from same class as the manager already in place or fall back to ``models.Manager`` if no manager exists.
