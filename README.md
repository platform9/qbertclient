# Platform9 Qbert client

This implementation of the Qbert client is an amalgam of various implementations in Platform9's internal tooling.
At the moment the goal is to get something out as quickly as possible.

# How to install
`pip install qbertclient`

# Usage

```
from qbertclient import qbert

qb = qbert.Qbert(token, 'https://<fqdn>/qbert/v3/<project_id>)
```
The client also exposes a simple Keystone client which allows users to get a Keystone token:
```
from qbertclient import qbert
from qbertclient import keystone

du_fqdn = "endpoint.platform9.net"
username = "username@platform9.net"
password = "hunter2"
project_name = "service"

keystone = keystone.Keystone(du_fqdn, username, password, project_name)
token = keystone.get_token()
project_id = keystone.get_project_id(project_name)

qb = qbert.Qbert(token, "https://{}/qbert/v3/{}".format(du_fqdn, project_id))
print(qb.list_clusters())
```
