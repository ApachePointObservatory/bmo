#!/usr/bin/env python2
# encoding: utf-8
#
# file.py
#
# Created by José Sánchez-Gallego on 17 Sep 2017.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import logging

from twisted.internet import reactor

import bmo.devices.fake_vimba
from bmo import config, __version__
from bmo.logger import log
from bmo.bmo_main import BMOActor

import click

# Import pymba, with import error exception.

try:
    import pymba
except (OSError, ImportError):
    pymba = None


@click.command()
@click.option('-t', '--test', is_flag=True, show_default=True,
              help='Test mode. Uses fake Vimba controller.')
@click.option('-d', '--debug', is_flag=True, show_default=True,
              help='Debug mode.')
def bmo_cmd(test=False, debug=False):

    port = config['tron']['port']

    if debug:
        log.sh.setLevel(logging.DEBUG)
        log.debug('BMO started in debug mode.')

    if test is False:
        assert pymba is not None, ('failed to import pymba module. '
                                   'Install pymba or run in test mode.')
        controller = pymba.Vimba()
    else:
        controller = bmo.devices.fake_vimba.Vimba()

    BMOActor(config, userPort=port, version=__version__,
             controller=controller, autoconnect=True)

    reactor.run()


if __name__ == '__main__':
    bmo_cmd()
