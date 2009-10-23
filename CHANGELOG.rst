===============================
Changelog for django-gatekeeper
===============================

0.3.0
=====

* added a moderation_reason field
* always use auto_moderator if set, ignoring GATEKEEPER_ENABLE_AUTOMODERATION
* reformat emails

0.2.2
=====

* add _gatekeeper attribute on GatekeeperQuerySet (for third party apps)
* BUGFIX: flag queries failing on postgres due to cast
* BUGFIX: import_unmoderated always found 0 objects to import

0.2.1
=====

* use GatekeeperManager for related access
* BUGFIX: wrong id for link in moderation list
* BUGFIX: fix GH #1, SQL error in trying to moderate objects with a generic fk

0.2.0
=====
* addition of flagging

    * new fields on ModeratedObject
    * small changes to the admin
    * new GATEKEEPER_STATUS_ON_FLAG setting

* addition of custom manager and properties added to registered models
* removal of gatekeeper.approved/rejected/pending (replaced by new filters on QuerySets)
* ModeratedObject field names changed

    * status - moderation_status
    * moderation_by - moderated_status_by 
    * moderation_date - moderation_status_date 

* BUGFIX: use DEFAULT_FROM_EMAIL for sending mail (was hardcoded address)
* BUGFIX: ModeratedObjectManager.get_for_instance

0.1.0
=====
* initial release, moderation and admin integration
