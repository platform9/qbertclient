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
This module contains the Qbert class
"""
import base64
import logging

from qbertclient import dict_utils, request_utils

LOG = logging.getLogger(__name__)


class Qbert():
    """
    The Qbert client to Platform9's Managed Kubernetes product.
    """

    def __init__(self, token, api_url):
        if not (token and api_url):
            raise ValueError('need a keystone token and API url')
        if api_url[-1] == '/':
            raise ValueError('API url must not have trailing slash')
        self.api_url = api_url
        self.token = token
        session = request_utils.session_with_retries(self.api_url)
        session.headers = {'X-Auth-Token': self.token,
                           'Content-Type': 'application/json'}
        self.session = session

    def _make_req(self, endpoint, method='GET', body={}):
        return request_utils.make_req(self.session, self.api_url + endpoint,
                                      method, body)

    def get_cloud_provider(self, uuid):
        """
        Get the details for a cloud provider account identified by the account uuid
        :param uuid: UUID of the cloud provider
        :return: json object
        """
        LOG.debug('Getting cloud provider region info for: %s', uuid)
        endpoint = '/cloudProviders/{0}'.format(uuid)
        resp = self._make_req(endpoint)
        return resp

    def get_cloud_provider_region_info(self, uuid, region):
        """
        Get the details for a region in a particular cloud provider account identified by the account uuid
        :param uuid: UUID of the cloud provider
        :param region: Name of the region
        :return:
        """
        LOG.debug('Getting cloud provider region info for: %s', uuid)
        endpoint = '/cloudProviders/{0}/region/{1}'.format(uuid, region)
        resp = self._make_req(endpoint)
        return resp

    def delete_cloud_provider(self, uuid):
        """
        Delete a cloud provider account specified by account uuid
        :param uuid: UUID of the cloud provider
        :return:
        """
        endpoint = '/cloudProviders/{0}'.format(uuid)
        method = 'DELETE'
        resp = self._make_req(endpoint, method)
        return resp

    def create_cloud_provider(self, request_body):
        """
        Create a cloud provider
        :param request_body:
        :return:
        """
        endpoint = '/cloudProviders'
        method = 'POST'
        resp = self._make_req(endpoint, method, request_body)
        return resp

    def update_cloud_provider(self, uuid, request_body):
        """
        Update a cloud provider
        :param uuid: UUID of the cloud provider
        :param request_body: JSON with cloud provider-specific fields to update
               'name' and 'type' are required fields regardless of cloud provider
        :return:
        """
        endpoint = '/cloudProviders/' + uuid
        method = 'PUT'
        resp = self._make_req(endpoint, method, request_body)
        return resp

    def list_cloud_providers(self):
        """
        List cloud providers
        :return:
        """
        LOG.debug('Listing Cloud Providers')
        endpoint = '/cloudProviders'
        resp = self._make_req(endpoint)
        return resp

    def list_cloud_provider_types(self):
        """
        List cloud provider types
        :return:
        """
        LOG.debug('Listing Cloud Provider Types')
        endpoint = '/cloudProvider/types'
        resp = self._make_req(endpoint)
        return resp

    def list_nodepools(self):
        """
        List nodepools
        :return:
        """
        LOG.debug('Listing node pools')
        endpoint = '/nodePools'
        resp = self._make_req(endpoint)
        return resp

    def list_nodes(self):
        """
        List nodes
        :return:
        """
        LOG.debug('Listing nodes')
        endpoint = '/nodes'
        resp = self._make_req(endpoint)
        return resp

    def list_nodes_by_uuid(self):
        """
        List nodes by uuid
        :return:
        """
        LOG.debug('Listing nodes')
        endpoint = '/nodes'
        resp = self._make_req(endpoint)
        return dict_utils.keyed_list_to_dict(resp, 'uuid')

    def list_clusters(self):
        """
        List clusters
        :return:
        """
        LOG.debug('Listing clusters')
        endpoint = '/clusters'
        resp = self._make_req(endpoint)
        return resp

    def list_clusters_by_uuid(self):
        """
        List clusters by uuid
        :return:
        """
        LOG.debug('Listing clusters')
        endpoint = '/clusters'
        resp = self._make_req(endpoint)
        return dict_utils.keyed_list_to_dict(resp, 'uuid')

    def update_cluster(self, uuid, body):
        """
        Update cluster
        :param uuid:
        :param body:
        :return:
        """
        LOG.debug('Updating cluster: %s', uuid)
        endpoint = '/clusters/' + uuid
        method = 'PUT'
        resp = self._make_req(endpoint, method, body)
        return resp

    def create_cluster(self, body):
        """
        Create cluster
        :param body:
        :return:
        """
        LOG.debug('Creating cluster %s', body['name'])
        endpoint = '/clusters'
        method = 'POST'
        resp = self._make_req(endpoint, method, body)
        return resp

    def get_cluster(self, uuid):
        """
        Get cluster by uuid
        :param uuid:
        :return:
        """
        LOG.debug('Get cluster')
        endpoint = '/clusters/%s' % uuid
        resp = self._make_req(endpoint)
        return resp

    def delete_cluster(self, uuid):
        """
        Delete cluster by uuid
        :param uuid:
        :return:
        """
        LOG.debug('Deleting cluster %s', uuid)
        endpoint = '/clusters/{0}'.format(uuid)
        method = 'DELETE'
        resp = self._make_req(endpoint, method)
        return resp

    def attach_nodes(self, nodes_list, cluster_name):
        """
        Attach node to cluster
        :param nodes_list:
        :param cluster_name:
        :return:
        """
        LOG.debug('Attaching nodes %s to cluster %s', nodes_list, cluster_name)
        nodes = self.list_nodes()
        node_uuids = [{'uuid': nodes[node_item['node_name']]['uuid'], 'isMaster': node_item['isMaster']} for node_item
                      in
                      nodes_list]
        cluster_uuid = self.list_clusters()[cluster_name]['uuid']
        endpoint = '/clusters/{0}/attach'.format(cluster_uuid)
        method = 'POST'
        body = node_uuids
        resp = self._make_req(endpoint, method, body)
        return resp

    def detach_node(self, node_name, cluster_name):
        """
        Detach node from cluster
        :param node_name:
        :param cluster_name:
        :return:
        """
        LOG.debug('Detaching node %s from cluster %s', node_name, cluster_name)
        node_uuid = [{'uuid': self.list_nodes()[node_name]['uuid']}]
        cluster_uuid = self.list_clusters()[cluster_name]['uuid']
        endpoint = '/clusters/{0}/detach'.format(cluster_uuid)
        method = 'POST'
        body = node_uuid
        resp = self._make_req(endpoint, method, body)
        return resp

    def attach_nodes_v2(self, node_names, cluster_name):
        """
        Attach node v2
        :param node_names:
        :param cluster_name:
        :return:
        """
        LOG.debug('Attaching nodes %s to cluster %s', node_names, cluster_name)
        nodes = self.list_nodes()
        node_uuids = [nodes[node_name]['uuid'] for node_name in node_names]
        cluster_uuid = self.list_clusters()[cluster_name]['uuid']
        endpoint = '/clusters/{0}/attach'.format(cluster_uuid)
        method = 'POST'
        body = node_uuids
        resp = self._make_req(endpoint, method, body)
        return resp

    def detach_node_v2(self, node_name, cluster_name):
        """
        Detach node v2
        :param node_name:
        :param cluster_name:
        :return:
        """
        LOG.debug('Detaching node %s from cluster %s', node_name, cluster_name)
        node_uuid = self.list_nodes()[node_name]['uuid']
        endpoint = '/nodes/{0}'.format(node_uuid)
        method = 'PUT'
        body = {'cluster_uuid': None}
        resp = self._make_req(endpoint, method, body)
        return resp

    def get_master_ip(self, cluster_uuid):
        """
        Get masterIP of a cluster with uuid cluster_uuid
        :param cluster_uuid:
        :return:
        """
        LOG.debug('Getting masterIp for cluster %s', cluster_uuid)
        return self.get_cluster(cluster_uuid)['masterIp']

    def get_kubeconfig(self, cluster_uuid, username='', password=''):
        """
        Get kubeconfig of a cluster by uuid. If both username and password
        are supplied, then configure kubeconfig to use password-based
        authentication, else use token.
        :param cluster_uuid:
        :param username: optional username
        :param password: optional password
        :return:
        """
        endpoint = '/kubeconfig/{0}'.format(cluster_uuid)
        resp = self._make_req(endpoint)
        if username and password:
            s = '{"username":"%s","password":"%s"}' % (username, password)
            token = base64.b64encode(s.encode()).decode()
        else:
            token = self.token
        kubeconfig = resp.text.replace('__INSERT_BEARER_TOKEN_HERE__', token)
        return kubeconfig

    def get_kubelog(self, node_name):
        """
        Get kubelog
        :param node_name:
        :return:
        """
        LOG.debug('Requesting kube.LOG from node %s', node_name)
        node_uuid = self.list_nodes()[node_name]['uuid']
        endpoint = '/LOGs/{0}'.format(node_uuid)
        resp = self._make_req(endpoint)
        # TODO: resp is not a Response object anymore,
        return resp.text

    def get_cli_token(self, cluster_uuid):
        """
        Get webcli token
        :param cluster_uuid:
        :return:
        """
        LOG.debug('Getting cli token for cluster %s', cluster_uuid)
        endpoint = '/webcli/{0}'.format(cluster_uuid)
        method = 'POST'
        resp = self._make_req(endpoint, method)
        return resp['token']

    def trigger_omniupgrade(self):
        """
        Trigger an omniupgrade
        :return:
        """
        LOG.debug('Triggering omniupgrade')
        endpoint = '/omniupgrade'
        method = 'POST'
        return self._make_req(endpoint, method)

    def upgrade_cluster(self, uuid):
        """
        Upgrade cluster by uuid
        :param uuid:
        :return:
        """
        LOG.debug('Upgrading cluster %s', uuid)
        endpoint = '/clusters/{0}/upgrade'.format(uuid)
        method = 'POST'
        body = {'batchUpgradePercent': 100}
        return self._make_req(endpoint, method, body)
