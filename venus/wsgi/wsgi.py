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

"""Venus OS API WSGI application."""


import sys
import warnings
from venus import objects
warnings.simplefilter('once', DeprecationWarning)
from oslo_config import cfg
from oslo_log import log as logging
from venus import i18n
i18n.enable_lazy()
# Need to register global_opts
from venus.common import config  # noqa
from venus import rpc
from venus import version
from venus.wsgi import common as wsgi_common

CONF = cfg.CONF


def _application():
    objects.register_all()
    CONF(sys.argv[1:], project='venus',
         version=version.version_string())
    logging.setup(CONF, "venus")

    rpc.init(CONF)
    return wsgi_common.Loader().load_app(name='osapi_venus')


application = _application()
