import os

import libcloud
from nanobox_libcloud.adapters import Adapter
from nanobox_libcloud.adapters.base import RebootMixin


class SoftLayerAdapter(RebootMixin, Adapter):
    """
    Adapter for IBM SoftLayer
    """

    # Adapter metadata
    id = "sl"
    name = 'IBM SoftLayer (Beta)'
    # server_nick_name = 'server'

    # Provider-wide server properties
    server_internal_iface = 'eth0'
    server_external_iface = 'eth1'

    # Provider auth properties
    auth_credential_fields = [
        ["Username", "Username"],
        ["Api-Key", "API Key"]
    ]
    auth_instructions = ""

    def __init__(self, **kwargs):
        self.generic_credentials = {
            'key': os.getenv('SL_USERNAME', ''),
            'secret': os.getenv('SL_API_KEY', '')
        }

    # Internal overrides for provider retrieval
    def _get_request_credentials(self, headers):
        """Extracts credentials from request headers."""

        return {
            "key": headers.get("Auth-Username", ''),
            "secret": headers.get("Auth-Api-Key", '')
        }

    def _get_user_driver(self, **auth_credentials):
        """Returns a driver instance for a user with the appropriate authentication credentials set."""

        driver = super()._get_user_driver(**auth_credentials)

        driver.list_nodes()

        return driver

    @classmethod
    def _get_id(cls):
        return 'softlayer'

    # Internal overrides for /meta
    def get_default_region(self):
        """Gets the default region ID."""

        return 'sea01'

    def get_default_size(self):
        """Gets the default size ID."""

        return '0'

    def get_default_plan(self):
        """Gets the default plan ID."""

        return 'standard'

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

        cpus = libcloud.compute.drivers.softlayer.SL_TEMPLATES.get(int(size.id), {}).get('cpus')

        if cpus:
            return float(cpus)

        return None

    # Internal overrides for /key endpoints
    def _create_key(self, driver, key):
        return driver.import_key_pair_from_string(key['id'], key['key'])

    # Internal overrides for /server endpoints
    def _get_create_args(self, data):
        """Returns the args used to create a server for this adapter."""

        driver = self._get_user_driver()

        location = self._find_location(driver, data['region'])
        size = self._find_size(driver, data['size'])

        return {
            'name': data['name'],
            'size': size,
            'location': location,
            'ex_domain': 'nanoapp.io',
            'ex_bandwidth': 100,
            'ex_os': 'UBUNTU_16',
            'ex_keyname': data['ssh_key']
        }
