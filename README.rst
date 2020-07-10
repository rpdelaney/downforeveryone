downforeveryone
======================
|LANGUAGE| |VERSION| |STYLE| |LICENSE| |CIRCLECI| |COVERAGE| |MAINTAINABILITY|
|MAINTAINED|

.. |CIRCLECI| image:: https://img.shields.io/circleci/build/gh/rpdelaney/downforeveryone
   :target: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master
.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
.. |MAINTAINED| image:: https://img.shields.io/maintenance/yes/2020?logoColor=informational
.. |VERSION| image:: https://img.shields.io/pypi/v/downforeveryone
   :target: https://pypi.org/project/downforeveryone
.. |STYLE| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |LANGUAGE| image:: https://img.shields.io/pypi/pyversions/downforeveryone
.. |COVERAGE| image:: https://img.shields.io/codeclimate/coverage/rpdelaney/downforeveryone
   :target: https://codeclimate.com/github/rpdelaney/downforeveryone
.. |MAINTAINABILITY| image:: https://img.shields.io/codeclimate/maintainability-percentage/rpdelaney/downforeveryone
   :target: https://codeclimate.com/github/rpdelaney/downforeveryone

Checks if a website is down for everyone or just you, via isup.me.

Installation
------------

.. code-block :: console

    pip3 install downforeveryone

============
Development
============

To install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_.

.. code-block :: console

    poetry install
    pre-commit install --install-hooks

Usage
-----

.. code-block :: console

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
