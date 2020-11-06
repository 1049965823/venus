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

"""Starter script for Naja Scheduler."""

from oslo_config import cfg
from oslo_log import log as logging
from oslo_reports import guru_meditation_report as gmr
from venus.common import config  # noqa
from venus import objects
from venus import service
from venus import utils
from venus import version
from venus import i18n
import eventlet
import sys

i18n.enable_lazy()
eventlet.monkey_patch()
# Need to register global_opts

CONF = cfg.CONF


def main():
    objects.register_all()
    CONF(sys.argv[1:], project='venus',
         version=version.version_string())
    logging.setup(CONF, "venus")
    from venus.task.timer import init_advanced_timer
    init_advanced_timer()
    # from venus.task import adapter
    # adapter.test_log_job()


if __name__ == "__main__":
    main()
