import pytest
from box_sdk_gen import BoxClient
from utils.box_client_ccg import (
    ConfigCCG,
    get_ccg_enterprise_client,
    get_ccg_user_client,
)


@pytest.fixture(scope="module")
def box_env_ccg() -> ConfigCCG:
    config = ConfigCCG()
    return config


@pytest.fixture(scope="module")
def box_client_ccg(box_env_ccg) -> BoxClient:
    client = get_ccg_enterprise_client(box_env_ccg)
    return client


@pytest.fixture(scope="module")
def box_client_ccg_user(box_env_ccg) -> BoxClient:
    client = get_ccg_user_client(box_env_ccg, box_env_ccg.ccg_user_id)
    return client
