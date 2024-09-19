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


class ConfigCCG:
    """application configurations"""

    def __init__(self) -> None:
        # Common configurations
        self.client_id = os.getenv("BOX_CLIENT_ID")
        self.client_secret = os.getenv("BOX_CLIENT_SECRET")

        # CCG configurations
        self.enterprise_id = os.getenv("BOX_ENTERPRISE_ID")
        self.ccg_user_id = os.getenv("BOX_USER_ID")

        self.cache_file = os.getenv("BOX_CACHE_FILE", ".ccg.tk")

        self.file_csv = os.getenv("FILE_CSV")
        self.file_template = os.getenv("FILE_TEMPLATE")
        self.folder_samples = os.getenv("FOLDER_SAMPLES")

        self.box_root_demo_folder = os.getenv("BOX_ROOT_DEMO_FOLDER")


def __repr__(self) -> str:
    return f"ConfigCCG({self.__dict__})"


def get_ccg_enterprise_client(config: ConfigCCG) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".ent" + config.cache_file),
    )
    auth = BoxCCGAuth(ccg)

    client = BoxClient(auth)

    return client


def get_ccg_user_client(config: ConfigCCG, user_id: str) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".user" + config.cache_file),
    )
    auth = BoxCCGAuth(ccg)
    auth = auth.with_user_subject(user_id)

    client = BoxClient(auth)

    return client


def whoami(client: BoxClient) -> User:
    user = client.users.get_user_me()
    return user
