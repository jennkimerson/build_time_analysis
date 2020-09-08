This tool analyzes ceph package build times in Brew.

Installing
==========

Create a Python virtualenv, activate it, and then run::

    pip install -r requirements.txt

On Fedora/RHEL, you can run without a virtualenv and use system-site packages
instead::

    sudo yum -y install \
      'python3dist(psycopg2)' \
      'python3dist(numpy)' \
      'python3dist(matplotlib)' \
      'python3dist(pandas)'
      
Kerberos and PostgreSQL
=======================

The Brew database is accessible through Teiid, a read-only virtual postgresql
interface to the main Brew PostgreSQL server.

You must have a Kerberos ticket to authenticate to the Teeid service running
on virtualdb.engineering.redhat.com.

To install ``kinit`` and ``klist`` on Fedora or RHEL, install the
``krb5-workstation`` package::

   sudo yum -y install krb5-workstation

To make Kerberos easier to use on your system, you can set
``default_realm = IPA.REDHAT.COM`` in ``/etc/krb5.conf``. Open it with an
editor in sudo mode::

   sudo vim /etc/krb5.conf

To get a Kerberos ticket, run the ``kinit`` command like so::

    kinit jenkim@IPA.REDHAT.COM

Check your Kerberos ticket cache with the ``klist -A`` command::

    klist -A

The output will look like this::

    $ klist -A
    Ticket cache: KCM:1000
    Default principal: jenkim@REDHAT.COM

    Valid starting       Expires              Service principal
    07/17/2020 15:39:14  07/18/2020 01:39:14  jenkim/REDHAT.COM@REDHAT.COM

PostgreSQL queries for Brew
===========================

To connect to Teeid on the command-line, you'll need the ``psql`` command.
Install it with yum::

    sudo yum -y install postgresql

Ensure you have a Kerberos ticket, and then run the ``psql`` command::

  psql -h virtualdb.engineering.redhat.com --port 5433 public

To view all of the Brew tables::

    SELECT vdbname, schemaname, name FROM tables WHERE schemaname='Brew' AND type='Table';

The "ceph" package entry in Brew has a package ID number of ``34590``. To query every build
record for the Ceph package::

    SELECT * FROM brew.build WHERE brew.build.pkg_id=34590;

Running
======

Before running this program, you must set the PGHOST environment::

    export PGHOST=virtualdb.engineering.redhat.com
    
There are 3 python scripts you can run to analyze the Ceph builds.

- To output all builds, containing the following information: id, package_id, version, release, start_time, completion_time, and build_duration::

    python3 view_stats.py

- To show the analysis of build time per each build_id in a form of scatter plot::

    python3 build_time_build_id.py

- Show the analysis of build time per build_version in a form of box plot::

    python3 build_time_ver.py


Running tests
=============

Install pytest in the virtualenv::

    pip install pytest

Run the tests::

    py.test

This should auto-discover any tests under the ``tests`` directory.
