#  Copyright 2019 Platform9
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
This module implements a few helpful methods for interfacing with the requests library.
"""

import logging
import os

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from qbertclient import exceptions as QbertExceptions

LOG = logging.getLogger(__name__)
REQUEST_TIMEOUT = int(os.getenv('HTTP_REQUEST_TIMEOUT_IN_SECS', '180'))


def session_with_retries(host, max_retries=10):
    """
    Return a session with retries
    :param host:
    :param max_retries:
    :return:
    """
    session = Session()
    http_statuses_to_retry = [
        502,  # Bad Gateway
        503,  # Service Unavailable
        504  # Gateway Timeout
    ]
    retries = Retry(total=max_retries, backoff_factor=1.0,
                    status_forcelist=http_statuses_to_retry)
    # HTTPAdapter's `max_retries` takes either an integer, or Retry object
    session.mount(host, HTTPAdapter(max_retries=retries))
    return session


def make_req(session, endpoint, method, body, verify=True):
    """
    Main request wrapper
    :param session:
    :param endpoint:
    :param method:
    :param body:
    :param verify:
    :return:
    """
    resp = session.request(method, endpoint, json=body, verify=verify,
                           timeout=REQUEST_TIMEOUT)
    LOG.debug('%s %s - %s', method, endpoint, resp.status_code)
    if 'application/json' in resp.headers.get('content-type'):
        obj = resp.json()
        if 'error' in obj:
            raise QbertExceptions.QbertError(obj['error']['message'])
        return obj
    else:
        return resp
