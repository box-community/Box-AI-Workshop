from pathlib import Path

from box_sdk_gen import BoxAPIError, BoxClient, File, PreflightFileUploadCheckParent


def file_upload(
    client: BoxClient, local_file_path: str, parent_folder_id: str, force: bool = False
) -> File:
    # check if file exists locally
    if not Path(local_file_path).exists():
        raise FileNotFoundError(f"File not found: {local_file_path}")

    size = Path(local_file_path).stat().st_size

    # Box preflight check if file already exists
    file_id = None
    try:
        parent = PreflightFileUploadCheckParent(id=parent_folder_id)
        client.uploads.preflight_file_upload_check(
            name=Path(local_file_path).name, size=size, parent=parent
        )
    except BoxAPIError as e:
        if e.response_info.code == "item_name_in_use":
            file_id = e.response_info.context_info.get("conflicts").get("id")
        else:
            raise e

    file_attributes = {
        "name": Path(local_file_path).name,
        "parent": {"id": parent_folder_id},
    }

    with open(local_file_path, "rb") as f:
        if file_id:
            if not force:
                return client.files.get_file_by_id(file_id)
            else:
                files = client.uploads.upload_file_version(
                    file_id=file_id, attributes=file_attributes, file=f
                )
            return files.entries[0]
        return client.uploads.upload_file(attributes=file_attributes, file=f).entries[0]


def file_delete(client: BoxClient, file_id: str):
    client.files.delete_file_by_id(file_id)
