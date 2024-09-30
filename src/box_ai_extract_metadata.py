from box_sdk_gen import (
    AiExtractResponse,
    AiItemBase,
    BoxClient,
    CreateAiExtractStructuredMetadataTemplate,
)
from tqdm import tqdm

from utils.box_client_ccg import AppConfig, get_ccg_user_client
from utils.box_metadata import apply_metadata_to_document
from utils.box_samples import files_start_with


def print_ai_response(prompt: str, ai_response: AiExtractResponse):
    print()
    print("=" * 80)
    print(f"Description: {prompt}")
    print("-" * 80)
    print(f"Answer:\n{ai_response}")
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

    hab_files = hab_1_files + hab_2_files + hab_3_files
    print(f"Using {len(hab_files)} documents for Box AI context")

    # Metadata template config
    template_key = "leases_workshop"
    template_type = "metadata_template"
    template_scope = f"enterprise_{conf.enterprise_id}"

    # Documents
    items = [AiItemBase(id=file.id, type="file") for file in hab_files]

    # Extract metadata from single document
    item = items[0]
    metadata_template = CreateAiExtractStructuredMetadataTemplate(
        template_key=template_key,
        type=template_type,
        scope=template_scope,
    )
    ai_response = client.ai.create_ai_extract_structured(
        items=[item],
        metadata_template=metadata_template,
    ).to_dict()
    print_ai_response("Extract metadata from single document", ai_response)

    # Apply metadata to document
    metadata = apply_metadata_to_document(client, item.id, template_key, ai_response)
    # filter out internal metadata items
    metadata = {
        k: v
        for k, v in metadata.to_dict().items()
        if (not k.startswith("$")) and (not k == "extra_data")
    }
    print_ai_response("Metadata applied to document:", metadata)

    # Extract metadata from multiple documents
    print(f"\nExtracting data from {len(items)} documents, and applying metadata...")
    progress_bar = tqdm(total=len(items))
    for item in items:
        # Extract document data using metadata template
        ai_response = client.ai.create_ai_extract_structured(
            items=[item],
            metadata_template=metadata_template,
        ).to_dict()

        # Apply metadata to document
        apply_metadata_to_document(client, item.id, template_key, ai_response)

        progress_bar.update()
    progress_bar.close()
    print()


if __name__ == "__main__":
    main()
