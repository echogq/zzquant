# coding: utf-8

"""
Copyright [zz.ai]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from .env import setup_environment_variables
from .version import get_version

from logging.handlers import RotatingFileHandler
import logging.handlers

setup_environment_variables()

version_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "version.info"))
if os.path.exists(version_file_path):
    with open(version_file_path, 'r') as version_file:
        __version__ = version_file.readline()
else:
    __version__ = get_version()


# 日志系统配置
# 1
file_log = os.path.dirname(os.path.abspath(__file__))+"zzq.log"
handler = RotatingFileHandler(file_log, maxBytes=1024 * 1024 * 10, backupCount=10, encoding='utf-8')
fmt = '%(asctime)s - %(filename)s:%(lineno)s - func: [%(name)s] - %(message)s'
# 2
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

log = logging.getLogger(__name__)

log.addHandler(handler)
log.setLevel(logging.DEBUG)

