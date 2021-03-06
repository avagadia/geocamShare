=========================================
GeoCam Share Tracking Module
=========================================

About
~~~~~

The ``shareLatitude`` app is a helper app for ``shareTracking`` that
handles authorizing Share to monitor user positions in Google Latitude
using OAuth, storing per-user access tokens, and requesting current
position and position history.

Installation
~~~~~~~~~~~~

Follow the normal directions for installing GeoCam Share.  If you're
updating an existing install that pre-dates ``shareLatitude``, you'll
need to re-run the following steps::

  # make sure shareLatitude dependencies are met (httplib2, oauth2)
  pip install -r $GEOCAM_DIR/share2/make/pythonRequirements.txt
  # install shareLatitude db tables
  $GEOCAM_DIR/share2/manage.py syncdb

Try It Out
~~~~~~~~~~

As a helper app, ``shareLatitude`` is not intended to provide a full
user interface, but for debugging purposes you can load
http://localhost:8000/latitude/ .  This is an index page with links that
allow you to authorize Share to monitor your position and test the
connection by viewing your current position according to Latitude.

| __BEGIN_LICENSE__
| Copyright (C) 2008-2010 United States Government as represented by
| the Administrator of the National Aeronautics and Space Administration.
| All Rights Reserved.
| __END_LICENSE__

