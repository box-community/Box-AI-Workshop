"""
Handles the box client object creation
orchestrates the authentication process
"""

import os

from box_sdk_gen import (
    BoxCCGAuth,
    BoxClient,
    CCGConfig,
    FileWithInMemoryCacheTokenStorage,
    User,
)

# ENV_CCG = ".ccg.env"
# ENV_CCG = None


class AppConfig:
    """application configurations"""

    def __init__(self) -> None:
        env_vars = {
            "client_id": "BOX_CLIENT_ID",
            "client_secret": "BOX_CLIENT_SECRET",
            "enterprise_id": "BOX_ENTERPRISE_ID",
            "ccg_user_id": "BOX_USER_ID",
            "cache_file": ("BOX_CACHE_FILE", ".auth.ccg"),
            "file_csv": "FILE_CSV",
            "file_template": "FILE_TEMPLATE",
            "folder_samples": "FOLDER_SAMPLES",
            "box_root_demo_folder": "BOX_ROOT_DEMO_FOLDER",
        }

        for attr, env_var in env_vars.items():
            if isinstance(env_var, tuple):
                setattr(self, attr, os.getenv(env_var[0], env_var[1]))
            else:
                setattr(self, attr, os.getenv(env_var))

    def __repr__(self) -> str:
        return f"ConfigCCG({self.__dict__})"

    __str__ = __repr__

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "client_secret"}


def __repr__(self) -> str:
    return f"ConfigCCG({self.__dict__})"


def get_ccg_enterprise_client(config: AppConfig) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.ent"),
    )
    auth = BoxCCGAuth(ccg)
    # print(f"Auth Enterprise: {auth.token_storage}")
    client = BoxClient(auth)
    return client


def get_ccg_user_client(config: AppConfig, user_id: str) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        # enterprise_id=config.enterprise_id,
        user_id=config.ccg_user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(f"{config.cache_file}.usr"),
    )
    auth = BoxCCGAuth(ccg)
    # print(f"Auth User: {auth.token_storage}")
    client = BoxClient(auth)
    return client


def whoami(client: BoxClient) -> User:
    user = client.users.get_user_me()
    return user
