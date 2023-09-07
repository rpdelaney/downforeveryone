downforeveryone
======================
|LANGUAGE| |VERSION| |LICENSE| |MAINTAINED| |BUILD| |STYLE|

.. |BUILD| image:: https://github.com/rpdelaney/downforeveryone/actions/workflows/main.yml/badge.svg
   :target: https://github.com/rpdelaney/downforeveryone/actions/workflows/main.yml
.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
.. |MAINTAINED| image:: https://img.shields.io/maintenance/yes/2023?logoColor=informational
.. |VERSION| image:: https://img.shields.io/pypi/v/downforeveryone
   :target: https://pypi.org/project/downforeveryone
.. |STYLE| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |LANGUAGE| image:: https://img.shields.io/pypi/pyversions/downforeveryone

Checks if a website is down for everyone or just you, via isup.me.

Installation
------------

.. code-block :: console

    pip3 install downforeveryone

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

============
Development
============

To install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_.

.. code-block :: console

    pre-commit install --install-hooks
    poetry install

`direnv <https://direnv.net/>`_ is optional, but recommended for convenience.

=================
Similar projects
=================
* `is-up-cli <https://github.com/sindresorhus/is-up-cli>`_: Same idea, but in Javascript.
