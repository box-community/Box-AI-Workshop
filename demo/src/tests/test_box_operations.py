import random
import string
import tempfile
from pathlib import Path

from box_sdk_gen import BoxClient
from utils.box import file_delete, file_upload
from utils.box_client_ccg import ConfigCCG


def test_box_file_upload(box_client_ccg_user: BoxClient, box_env_ccg: ConfigCCG):
    client = box_client_ccg_user
    conf = box_env_ccg
    # create temporary random file
    file_content = "".join(random.choices(string.ascii_lowercase, k=1000))
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(file_content.encode())
    temp_file.close()

    # upload file
    file = file_upload(client, temp_file.name, conf.box_root_demo_folder)
    assert file is not None
    assert file.id is not None
    first_file_id = file.id
    first_version_id = file.file_version.id

    # upload file again no force (skip upload)
    file = file_upload(client, temp_file.name, conf.box_root_demo_folder)
    assert file is not None
    assert file.id is not None
    assert file.id == first_file_id
    assert file.file_version.id == first_version_id

    # upload file again force (new version)
    file = file_upload(client, temp_file.name, conf.box_root_demo_folder, force=True)
    assert file is not None
    assert file.id is not None
    assert file.id == first_file_id
    assert file.file_version.id != first_version_id

    # delete temporary file from box
    file_delete(client, first_file_id)

    # delete temporary file
    Path(temp_file.name).unlink()
    assert not Path(temp_file.name).exists()
