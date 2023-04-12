import importlib
import os
import typing

from microbox_libcloud.adapters.base import Adapter, AdapterBase


def get_adapter(adapter_id: str) -> typing.Optional[Adapter]:
    """Returns the adapter with the given id or `None` if there is none."""
    adapter = AdapterBase.registry.get(adapter_id)
    if adapter:
        return adapter()
    return None


def import_adapters():
    """Finds and imports modules containing adapter implementations."""
    for file in os.listdir(os.path.dirname(__file__)):
        if not file.startswith('_') and file.endswith('.py'):
            importlib.import_module('{}.{}'.format(__name__, file[:-3]))


# Import all modules containing adapters so they will be registered
import_adapters()
