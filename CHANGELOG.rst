===============================
Changelog for django-gatekeeper
===============================

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
