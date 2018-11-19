import os

import libcloud
from nanobox_libcloud.adapters import Adapter
# from nanobox_libcloud.adapters.base import RebootMixin


class __Adapter(Adapter):
    """
    Adapter for __
    """

    # Adapter metadata
    id = "__"
    name = '__ (Beta)'
    # server_nick_name = 'server'

    # Provider-wide server properties
    # server_internal_iface = 'eth1'
    # server_external_iface = 'eth0'
    # server_ssh_user = 'root'
    # server_ssh_auth_method = 'key'
    # server_ssh_key_method = 'reference'
    # server_bootstrap_script = 'https://s3.amazonaws.com/tools.nanobox.io/bootstrap/ubuntu.sh'
    # server_bootstrap_timeout = None

    # Provider auth properties
    auth_credential_fields = [
        ["", ""]
    ]
    auth_instructions = ""

    def __init__(self, **kwargs):
        self.generic_credentials = {
            'key': os.getenv('__', '')
        }

    # Internal overrides for provider retrieval
    def _get_request_credentials(self, headers):
        """Extracts credentials from request headers."""

        return {
            "key": headers.get("Auth-", '')
        }

    # @classmethod
    # def _get_id(cls):
    #     return '__'

    # Internal overrides for /meta
    def get_default_region(self):
        """Gets the default region ID."""

        return ''

    def get_default_size(self):
        """Gets the default size ID."""

        return ''

    def get_default_plan(self):
        """Gets the default plan ID."""

        return ''

    # Internal overrides for /catalog
    def _get_plans(self, location):
        """Retrieves a list of plans."""

        return [('standard', 'Standard')]

    def _get_sizes(self, location, plan):
        """Retrieves a list of sizes."""

        return self._get_generic_driver().list_sizes(location)

    @classmethod
    def _get_cpu(cls, location, plan, size):
        """Returns a CPU count value for a given adapter as a ServerSpec value."""

        if size.extra['??']:
            return float(size.extra['??'])

        return None

    # Internal overrides for /server endpoints
    def _get_create_args(self, data):
        """Returns the args used to create a server for this adapter."""

        return {
            'name': data['name'],
            # 'size': None,
            # 'image': None,
            # 'location': None
        }
