This tool analyzes ceph package build times in Brew.

Installing
==========

Create a Python virtualenv, activate it, and then run::

    pip install -r requirements.txt


Kerberos and PostgreSQL
=======================

The Brew database is accessible through Teiid, a read-only virtual postgresql
interface to the main Brew PostgreSQL server.

You must have a Kerberos ticket to authenticate to the Teeid service running
on virtualdb.engineering.redhat.com.

To install ``kinit`` and ``klist`` on Fedora or RHEL, install the
``krb5-workstation`` package::

   yum -y install krb5-workstation

To make Kerberos easier to use on your system, you can set
``default_realm = IPA.REDHAT.COM`` in ``/etc/krb5.conf``.

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

To connect to Teeid on the command-line, ensure you have a Kerberos ticket,
and then run the ``psql`` command::

  psql -h virtualdb.engineering.redhat.com --port 5433 public

To view all of the Brew tables::

    SELECT vdbname, schemaname, name FROM tables WHERE schemaname='Brew' AND type='Table';

The "ceph" package entry in Brew has a package ID number of ``34590``. To query every build
record for the Ceph package::

    SELECT * FROM brew.build WHERE brew.build.pkg_id=34590;

Running tests
=============

Install pytest in the virtualenv::

    pip install pytest

Run the tests::

    py.test

This should auto-discover any tests under the ``tests`` directory.
