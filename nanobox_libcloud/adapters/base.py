import typing

import libcloud
from libcloud.compute.types import Provider

from nanobox_libcloud.utils import models


class AdapterBase(type):
    """
    Metaclass for Adapter classes registering defined adapters.
    """
    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super(AdapterBase, mcs).__new__(mcs, name, bases, attrs)
        if name != 'Adapter':
            mcs.register(cls)
        return cls

    @classmethod
    def register(mcs, cls):
        adapter_id = cls.get_id()

        # Check if there is an existing adapter with the same id
        if adapter_id in mcs.registry:
            raise ValueError(
                "Cannot register adapter {}, there already exists an adapter with id {}.".format(
                    cls.__name__,
                    adapter_id,
                )
            )

        # Actually register the adapter
        mcs.registry[adapter_id] = cls


class Adapter(object, metaclass=AdapterBase):
    """
    Base class for Nanobox libcloud adapters. Implements basic functionality that should work for most libcloud drivers
    which can be overridden by subclasses for specific drivers.

    If subclasses are placed in the same package as this module they will automatically be discovered.
    """
    # Adapter metadata
    id = None  # type: str
    name = ''  # type: str
    server_nick_name = 'server'  # type: str

    # Provider-wide server properties
    server_internal_iface = 'eth1'  # type: str
    server_external_iface = 'eth0'  # type: str
    server_ssh_user = 'root'  # type: str
    server_ssh_auth_method = 'key'  # type: str
    server_ssh_key_method = 'reference'  # type: str
    server_bootstrap_script = 'https://s3.amazonaws.com/tools.nanobox.io/bootstrap/ubuntu.sh'  # type: str

    # Provider auth properties
    auth_credential_fields = []  # type: typing.Tuple[str, str]
    auth_instructions = ""  # type: str

    def __init__(self, **auth_credentials):
        self._driver = self.get_driver_class()(**auth_credentials)

    def get_meta(self) -> models.AdapterMeta:
        """Returns the metadata of this adapter."""
        return models.AdapterMeta(
            id=self.id,
            name=self.name,
            server_nick_name=self.server_nick_name,
            default_region=self.get_default_region(),
            default_size=self.get_default_size(),
            default_plan=self.get_default_plan(),
            can_reboot=self.can_reboot(),
            can_rename=self.can_rename(),
            internal_iface=self.server_internal_iface,
            external_iface=self.server_external_iface,
            ssh_user=self.server_ssh_user,
            ssh_auth_method=self.server_ssh_auth_method,
            ssh_key_method=self.server_ssh_key_method,
            bootstrap_script=self.server_bootstrap_script,
            auth_credential_fields=self.auth_credential_fields,
            auth_instructions=self.auth_instructions,
        )

    def get_catalog(self) -> typing.List[models.ServerRegion]:
        """Returns the catalog for this adapter."""
        pass  # TODO

    @classmethod
    def get_driver_class(cls) -> typing.Type[Provider]:
        """Returns the libcloud driver class for the id of this adapter."""
        return libcloud.get_driver(libcloud.DriverType.COMPUTE, cls.get_id())

    @classmethod
    def get_id(cls) -> str:
        """"Returns the id of this adapter."""
        if not cls.id:
            cls._config_error("No id set for adapter {cls}.")
        return cls.id

    @classmethod
    def get_default_region(cls) -> str:
        """Returns the id of the default region for this adapter."""
        raise NotImplementedError()

    @classmethod
    def get_default_size(cls) -> str:
        """Returns the id of the default server size for this adapter."""
        raise NotImplementedError()

    @classmethod
    def get_default_plan(cls) -> str:
        """Returns the id of the default plan for this adapter."""
        raise NotImplementedError()

    @classmethod
    def can_reboot(cls) -> bool:
        """Returns whether this adapter allows servers to be rebooted."""
        return hasattr(cls, 'reboot_server') and callable(cls.reboot_server)

    @classmethod
    def can_rename(cls) -> bool:
        """Returns whether this adapter allows servers to be renamed."""
        return hasattr(cls, 'rename_server') and callable(cls.rename_server)

    @classmethod
    def _config_error(cls, msg, **kwargs):
        raise ValueError(msg.format(cls=cls.__name__, **kwargs))


class RebootMixin(object):
    """
    Mixin for adapters to signify that servers can be rebooted.
    """
    @classmethod
    def reboot_server(cls, server):
        raise NotImplementedError()


class RenameMixin(object):
    """
    Mixin for adapters to signify that servers can be renamed.
    """
    @classmethod
    def rename_server(cls, server):
        raise NotImplementedError()
