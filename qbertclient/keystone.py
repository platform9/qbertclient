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
This modu_fqdnle contains the Keystone class.
"""

import json
import logging

import requests

LOG = logging.getLogger(__name__)


class Keystone():
    """
    The Keystone class which implements a simple Keystone client
    """

    def __init__(self, du_fqdn, username, password, project_name, mfa_token=None, verify=True):
        self.du_fqdn = du_fqdn
        self.username = username
        self.password = password
        self.project_name = project_name
        self.mfa_token = mfa_token
        self.verify = verify
        self.token = None

    def get_token(self):
        """
        The python keystoneclient doesn't provide a way to get a v3 nocatalog
        token, so this function gets one from the api.
        """
        url = "https://{}/keystone/v3/auth/tokens?nocatalog".format(self.du_fqdn)

        methods = ['password']
        totp_body = None
        if self.mfa_token:
            methods.append('totp')
            totp_body = {
                "user": {
                    "name": self.username,
                    "domain": {
                        "id": "default"
                    },
                    "passcode": self.mfa_token
                }
            }
        body = {
            "auth": {
                "identity": {
                    "methods": methods,
                    "password": {
                        "user": {
                            "name": self.username,
                            "domain": {
                                "id": "default"
                            },
                            "password": self.password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": self.project_name,
                        "domain": {"id": "default"}
                    }
                }
            }
        }

        if totp_body:
            body['auth']['identity']['totp'] = totp_body

        LOG.debug("Printing login body: {}".format(body))
        resp = requests.post(url,
                             data=json.dumps(body),
                             headers={'content-type': 'application/json'},
                             verify=self.verify)
        resp.raise_for_status()
        LOG.debug("Printing login response: {}".format(resp.json()))
        self.token = resp.headers['X-Subject-Token']
        return self.token

    def get_project_id(self, project_name=None):
        """
        Return the project id of a project named project_name
        :param project_name: The name of the project
        :return:
        """
        url = "https://{}/keystone/v3/projects".format(self.du_fqdn)
        resp = requests.get(url, verify=self.verify,
                            headers={'X-Auth-Token': self.token,
                                     'Content-Type': 'application/json'})
        projects = resp.json()['projects']
        for project in projects:
            if project['name'] == project_name:
                return project['id']
        return None
