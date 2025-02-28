import pytest
from traitlets import TraitError
from repo2docker.engine import ContainerEngine


def test_registry_credentials():
    e = ContainerEngine(parent=None)

    # This should be fine
    e.registry_credentials = {"registry": "something", "username": "something", "password": "something"}

    with pytest.raises(TraitError):
        e.registry_credentials = {"hi": "bye"}
