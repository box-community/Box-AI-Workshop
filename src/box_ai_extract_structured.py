from typing import List

from box_sdk_gen import (
    AiExtractResponse,
    AiItemBase,
    BoxClient,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
)
from tqdm import tqdm

from utils.box_ai_structured import FieldType, LeaseDocument
from utils.box_client_ccg import AppConfig, get_ccg_user_client
from utils.box_samples import files_start_with


def print_ai_response(prompt: str, ai_response: AiExtractResponse):
    print()
    print("=" * 80)
    print(f"Prompt: {prompt}")
    print("-" * 80)
    print(f"Answer:\n{ai_response.to_dict()}")
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

    # Sample data
    # Property id: HAB-3-04
    # Property type: HAB-3
    # Lease Start Date: 2024-05-01
    # Lease End Date: 2027-04-30
    # Monthly Rent: 4,250.00
    # Property Address: Schiaparelli Plaza Property
    # Lessee Name: Max Planck
    # Lessee Email: max.planck@moonhabitat.space
    # Lessor Name: Schiaparelli plaza
    # Agreement Date: 2024-04-21
    # Agreement Term: 3 years
    # Number of bedrooms: 3

    # Documents
    items = [AiItemBase(id=file.id, type="file") for file in hab_files]
    item = items[0]

    # Build the structured prompt
    fields: List[CreateAiExtractStructuredFields] = []

    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING, key="property_id", prompt="Property id"
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING,
            key="property_type",
            prompt="Property type",
            options=[
                CreateAiExtractStructuredFieldsOptionsField(key="HAB-1"),
                CreateAiExtractStructuredFieldsOptionsField(key="HAB-2"),
                CreateAiExtractStructuredFieldsOptionsField(key="HAB-3"),
            ],
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.DATE,
            key="lease_start_date",
            prompt="Lease Start Date in YYYY-MM-DD format",
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.DATE,
            key="lease_end_date",
            prompt="Lease End Date in YYYY-MM-DD format",
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.FLOAT,
            key="monthly_rent",
            prompt="Monthly Rent as a float including cents",
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING, key="property_address", prompt="Property Address"
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING, key="lessee_name", prompt="Lessee Name"
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING, key="lessee_email", prompt="Lessee Email"
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.STRING, key="lessor_name", prompt="Lessor Name"
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.DATE,
            key="agreement_date",
            prompt="Agreement Date in YYYY-MM-DD format",
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.INTEGER,
            key="agreement_term",
            prompt="Agreement Term in years",
        )
    )
    fields.append(
        CreateAiExtractStructuredFields(
            type=FieldType.INTEGER,
            key="number_of_bedrooms",
            prompt="Number of bedrooms as an integer",
        )
    )

    # Extract data from single document
    ai_response: AiExtractResponse = client.ai.create_ai_extract_structured(
        items=[item], fields=fields
    )
    print_ai_response("Extract data from document", ai_response)

    # multiple documents
    sample_leases: List[LeaseDocument] = []
    print(f"\nExtracting data from {len(items)} documents...")
    progress_bar = tqdm(total=len(items))
    for idx, item in enumerate(items):
        ai_response = client.ai.create_ai_extract_structured(
            items=[item], fields=fields
        )
        sample_leases.append(LeaseDocument(**ai_response.to_dict()))
        progress_bar.update()
    progress_bar.close()
    print()

    print("Sample Leases:")
    for idx, lease in enumerate(sample_leases, 1):
        print(f"Document {idx}:")
        print(lease)
        print()


if __name__ == "__main__":
    main()
