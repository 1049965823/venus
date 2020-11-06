# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Starter script for All venus services.

This script attempts to start all the venus services in one process.  Each
service is started in its own greenthread.  Please note that exceptions and
sys.exit() on the starting of a service are logged and the script will
continue attempting to launch the rest of the services.

"""

from oslo_config import cfg

from oslo_log import log as logging

from oslo_reports import guru_meditation_report as gmr

from venus.common import config  # noqa

from venus.i18n import _LE

from venus import objects

from venus import rpc

from venus import service

from venus import utils

from venus import version

from venus import i18n

import eventlet

import sys

eventlet.monkey_patch()
i18n.enable_lazy()

CONF = cfg.CONF


# TODO(e0ne): get a rid of code duplication in venus.cmd module in Mitaka
def main():
    objects.register_all()
    CONF(sys.argv[1:], project='venus',
         version=version.version_string())
    logging.setup(CONF, "venus")
    log = logging.getLogger('venus.all')

    utils.monkey_patch()

    gmr.TextGuruMeditation.setup_autorun(version)

    rpc.init(CONF)

    launcher = service.process_launcher()
    # venus-api
    try:
        server = service.WSGIService('osapi_venus')
        launcher.launch_service(server, workers=server.workers or 1)
    except (Exception, SystemExit):
        log.exception(_LE('Failed to load osapi_venus'))

    # venus-venusmanager
    try:
        launcher.launch_service(
            service.Service.create(binary="venus-venusmanager"))
    except (Exception, SystemExit):
        log.exception(_LE('Failed to load venus-venusmanager'))

    launcher.wait()
