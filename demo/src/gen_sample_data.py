from pathlib import Path

from box_sdk_gen import File, Folder
from tqdm import tqdm
from utils.box import file_upload, folder_create
from utils.box_client_ccg import ConfigCCG, get_ccg_user_client, whoami
from utils.create_samples import execute_mail_merge


def main():
    # execute mail merge
    execute_mail_merge()

    # get box user client
    conf = ConfigCCG()
    print(f"\nConfiguration:\n{conf.to_dict()}")

    # get ccg user client
    print("\nGetting CCG user client..")
    client = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    user = whoami(client)
    print(f"Who am I: {user.name} (id: {user.id})")

    # create samples folder in box
    print("\nCreating sample folders:")
    sample_folder: Folder = folder_create(
        client=client,
        parent_folder_id=conf.box_root_demo_folder,
        folder_name="Habitat Leases",
    )
    print(f"Sample folder: {sample_folder.id}")

    # read local sample files and upload to box
    print("\nUploading sample files:")
    total_bytes = sum(f.stat().st_size for f in Path(conf.folder_samples).iterdir())
    progress_bar = tqdm(total=total_bytes, unit="B", unit_scale=True)

    for sample_file in Path(conf.folder_samples).iterdir():
        file: File = file_upload(
            client=client,
            local_file_path=sample_file.as_posix(),
            parent_folder_id=sample_folder.id,
        )
        progress_bar.update(sample_file.stat().st_size)
    progress_bar.close()
    print()


if __name__ == "__main__":
    main()
