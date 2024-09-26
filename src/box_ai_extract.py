import json
from typing import List

from box_sdk_gen import AiItemBase, AiResponseFull, BoxClient
from tqdm import tqdm

from utils.box_client_ccg import AppConfig, get_ccg_user_client
from utils.box_samples import files_start_with


def print_ai_response(prompt: str, ai_response: AiResponseFull):
    print()
    print("=" * 80)
    print(f"Prompt: {prompt}")
    print("-" * 80)
    print(f"Answer:\n{ai_response.answer}")
    print("=" * 80)
    print()


def main():
    conf = AppConfig()
    client: BoxClient = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    me = client.users.get_user_me()
    # cleat screen
    print("\033[H\033[J")
    print(f"Hello, I'm logged in as {me.name} ({me.id})")

    # find files starting with 'HAB-1' in Habitat Leases folder
    hab_1_files = files_start_with("HAB-1", client, conf)
    hab_2_files = files_start_with("HAB-2", client, conf)
    hab_3_files = files_start_with("HAB-3", client, conf)

    # select 10% of each files into a single list
    hab_files = (
        hab_1_files[: int(len(hab_1_files) * 0.4)]
        + hab_2_files[: int(len(hab_2_files) * 0.4)]
        + hab_3_files[: int(len(hab_3_files) * 0.4)]
    )
    print(f"Using {len(hab_files)} documents for Box AI context")

    # Extract data from single document
    prompt = f"Extract data from document {hab_files[0].name}"
    items = [AiItemBase(id=hab_files[0].id, type="file")]
    ai_response = client.ai.create_ai_extract(prompt=prompt, items=items)
    print_ai_response(prompt, ai_response)

    # create an output for each document
    output: List[AiResponseFull] = []

    prompt = (
        "Lease Start Date, Lease End Date, Monthly Rent, Property Address,"
        "Lessee Name, Lessee Email, Lessor Name, Agreement Date, "
        "Agreement Term, Number of bed rooms as an integer, "
        "all dates should be in format yyyy-mm-dd"
    )
    items = [AiItemBase(id=file.id, type="file") for file in hab_files]

    print(f"Extracting data from {len(items)} documents...")
    progress_bar = tqdm(total=len(items))
    for idx, item in enumerate(items):
        ai_response = client.ai.create_ai_extract(prompt=prompt, items=[item])
        output.append(json.loads(ai_response.answer))
        progress_bar.update()
    progress_bar.close()
    print()

    print("Output:")
    for idx, data in enumerate(output, 1):
        print(f"Document {idx}:")
        for key, value in data.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    main()
