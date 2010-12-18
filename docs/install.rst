=========================================
GeoCam Share Installation
=========================================

These installation instructions are a work in progress.  If you follow
the directions and run into problems, let us know!

We will go through two versions of the installation:

1. Basic installation using Django's built-in development web server and
a SQLite database.  This version is only suitable for quick testing due
to security and performance issues.

2. Advanced installation using the Apache web server and a MySQL
database.  This version is intended for real deployments.

Requirements
~~~~~~~~~~~~

Our primary development platform for GeoCam Share is Ubuntu Linux 10.04
(Lucid Lemur), running Python 2.6 and Django 1.2.  For the basic
installation we use Django's built-in development web server with a
SQLite 3.6 database.  For the advanced installation we use the Apache
2.2 web server hosting Python using modwsgi 2.8, with a MySQL 5.1
database.

We have also successfully installed parts of GeoCam Share on RedHat
Enterprise Linux 5.5 and Mac OS X 10.6 (Snow Leopard).  However, we do
not officially support those platforms.  Our installation instructions
below mostly assume Ubuntu, so if you want to use another platform
you may need to improvise more during installation.

Set Up an Install Location
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create a directory to hold the whole Share installation
and capture the path in an environment variable we can use
in the instructions below::

  export GEOCAM_DIR=$HOME/projects/geocam # or choose your own
  mkdir -p $GEOCAM_DIR

Get the Source
~~~~~~~~~~~~~~

Visit the `GeoCam Share repository on GitHub`_, click on the Downloads_
button, and click on "Download .tar.gz" to get a tarball.  Then drop the
tarball into the ``$GEOCAM_DIR`` directory and run::

  cd $GEOCAM_DIR
  tar xfz geocam-geocamShare-*.tar.gz
  # rename the resulting directory to "share2"
  mv `ls -d geocam-geocamShare-* | head -1` share2

.. _GeoCam Share repository on GitHub: http://github.com/geocam/geocamShare/
.. _Downloads: http://github.com/geocam/geocamShare/archives/master

**Advanced version:** If you're interested in contributing code to GeoCam
Share, you can check out our latest revision with::

  cd $GEOCAM_DIR
  git clone http://github.com/geocam/geocamShare.git share2

For more information on the Git version control system, visit `the Git home page`_.
You can install Git on Ubuntu with::

  sudo apt-get install git-core

.. _the Git home page: http://git-scm.com/

Optionally Install virtualenv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Especially for a quick test install, we recommend using the virtualenv_
tool to put Share-related Python packages in an isolated sandbox where
they won't conflict with other Python tools on your system.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv

To install virtualenv, create a sandbox named ``packages``, and
"activate" the sandbox::

  sudo apt-get install python-virtualenv
  cd $GEOCAM_DIR
  virtualenv packages
  source packages/bin/activate

After your sandbox is activated, package management tools such as
``easy_install`` and ``pip`` will install packages into your sandbox
rather than the standard system-wide Python directory, and the Python
interpreter will know how to import packages installed in your sandbox.

You'll need to source the ``activate`` script every time you log in
to reactivate the sandbox.

Install Dependencies (Basic Version)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First install Ubuntu packages::

  # tools for Python package compilation and management
  sudo apt-get install python2.6-dev python-pip

  # basic database
  sudo apt-get sqlite3 libsqlite3-dev
  
  # rendering icons and reading image metadata
  sudo apt-get install libjpeg-dev libimage-exiftool-perl imagemagick

Then install Python dependencies.  Before running this command, you will
either need to activate your virtualenv environment (recommended) or
become root::

  pip install -r $GEOCAM_DIR/share2/make/pythonRequirements.txt

Set Up GeoCam Share
~~~~~~~~~~~~~~~~~~~

To render icons and collect media for the server, run::

  cd $GEOCAM_DIR/share2
  python setup.py install

Note that, maybe confusingly, this is not a standard Python install
script.  The action it takes is more like "build" than "install".  It
does not modify anything outside the ``share2`` directory.

To initialize the database, run::

  cd $GEOCAM_DIR/share2
  ./manage.py syncdb

The syncdb script will ask you if you want to create a Django superuser.
We recommend answering 'yes' and setting the admin username to 'root'
for compatibility with our utility scripts.

Import Sample Data
~~~~~~~~~~~~~~~~~~



Install Dependencies (Advanced Version)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First install Ubuntu packages::

  # web server
  sudo apt-get install apache2 libapache2-mod-wsgi

  # database
  sudo apt-get install mysql-server

Then install Python packages.  For this command to work, you will either
need to activate your virtualenv environment or become root::

  pip install MySQL-python==1.2.2

Foo
~~~

Further steps, not yet documented:

 * Modify local_settings.py to connect to your database
 * Add server to your Apache config

| __BEGIN_LICENSE__
| Copyright (C) 2008-2010 United States Government as represented by
| the Administrator of the National Aeronautics and Space Administration.
| All Rights Reserved.
| __END_LICENSE__