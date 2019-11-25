downforeveryone
======================
|CIRCLECI| |LICENSE|

.. |CIRCLECI| image:: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master.svg?style=svg
   :target: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master
.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt

Checks if a website is down for everyone or just you, via isup.me.

Installation
------------

::

    pip3 install downforeveryone

============
Development
============

To install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_.

::

    poetry install
    pre-commit install --install-hooks

Usage
-----

::

    $ isup -h
    usage: isup [-h] url

    checks if a site is down for everyone or just you

    positional arguments:
    url         url to test

    optional arguments:
    -h, --help  show this help message and exit
    $ isup google.com ; echo $?
    just you.
    1
    $ isup thingthatsdown.com ; echo $?
    it's down.
    0
