koosli.org [![Build Status](https://travis-ci.org/Koosli/koosli.org.svg?branch=master)](https://travis-ci.org/Koosli/koosli.org)
==========

Autonomous search platform with good intentions.


Development
-----------

Install virtualenv, then:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r dev-requirements.txt
    $ python run_devserver.py

To run the tests:

    $ nosetests

Keep [test coverage](http://koosli.github.io/koosli.org/) up.


Vagrant
-------

To run a full virtual environment, install VirtualBox and Vagrant, add the following to your hosts
file:

    10.10.10.33 koosli.dev
    10.10.10.33 www.koosli.dev

Spin up the vagrant env:

    $ vagrant up

Build and deploy the app:

    $ python setup.py sdist --formats gztar
    $ fab deploy_vagrant

**Note:** `deploy_vagrant` is just an alias for `deploy` with the host configured to `vagrant:vagrant@10.10.10.33`
