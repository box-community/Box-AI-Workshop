from typing import Dict

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateFileMetadataByIdScope,
    CreateMetadataTemplateFields,
    CreateMetadataTemplateFieldsOptionsField,
    CreateMetadataTemplateFieldsTypeField,
    MetadataFull,
    MetadataTemplate,
    UpdateFileMetadataByIdRequestBody,
    UpdateFileMetadataByIdRequestBodyOpField,
    UpdateFileMetadataByIdScope,
)


def get_template_by_key(client: BoxClient, template_key: str) -> MetadataTemplate:
    """Get a metadata template by key"""

    scope = "enterprise"

    try:
        template = client.metadata_templates.get_metadata_template(
            scope=scope, template_key=template_key
        )
    except BoxAPIError as err:
        if err.response_info.status_code == 404:
            template = None
        else:
            raise err

    return template


def delete_template_by_key(client: BoxClient, template_key: str):
    """Delete a metadata template by key"""

    scope = "enterprise"

    try:
        client.metadata_templates.delete_metadata_template(
            scope=scope, template_key=template_key
        )
    except BoxAPIError as err:
        if err.response_info.status_code == 404:
            pass
        else:
            raise err


def create_leases_template(
    client: BoxClient, template_key: str, display_name: str
) -> MetadataTemplate:
    """Create a metadata template"""

    # fields
    # {
    #     "property_address": "Schiaparelli Plaza Property",
    ##     "number_of_bedrooms": 1,
    ##     "lessee_email": "marie.tharp@moonhabitat.space",
    ##     "lessee_name": "Marie Tharp",
    ##     "agreement_date": "2024-04-24",
    ##     "lease_start_date": "2024-05-01",
    ##     "lease_end_date": "2027-04-30",
    ##     "monthly_rent": 3125,
    ##     "property_type": "HAB-1",
    #     "lessor_name": "Schiaparelli plaza",
    ##     "agreement_term": 3,
    ##     "property_id": "HAB-1-01",
    # }

    scope = "enterprise"

    fields = []

    # property_id
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="property_id",
            display_name="Property id",
        )
    )

    # property_type
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.ENUM,
            key="property_type",
            display_name="Property type",
            description="Property topology (HAB-1, HAB-2, or HAB-3)",
            options=[
                CreateMetadataTemplateFieldsOptionsField(key="HAB-1"),
                CreateMetadataTemplateFieldsOptionsField(key="HAB-2"),
                CreateMetadataTemplateFieldsOptionsField(key="HAB-3"),
                CreateMetadataTemplateFieldsOptionsField(key="Unknown"),
            ],
        )
    )

    # agreement_date
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.DATE,
            key="agreement_date",
            display_name="Agreement date",
            description="Agreement date in YYYY-MM-DDT00:00:00Z format",
        )
    )

    # lease_start_date
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.DATE,
            key="lease_start_date",
            display_name="Lease start date",
            description="Lease start date in YYYY-MM-DDT00:00:00Z format",
        )
    )

    # lease_end_date
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.DATE,
            key="lease_end_date",
            display_name="Lease end date",
            description="Lease end date in YYYY-MM-DDT00:00:00Z format",
        )
    )

    # monthly_rent
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            key="monthly_rent",
            display_name="Monthly rent",
            description="Monthly rent as a float including cents",
        )
    )

    # number_of_bedrooms
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            key="number_of_bedrooms",
            display_name="Number of bedrooms",
            description="Number of bedrooms for this property",
        )
    )

    # agreement_term
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            key="agreement_term",
            display_name="Agreement term (years)",
            description="Agreement term in years",
        )
    )

    # lessee_name
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="lessee_name",
            display_name="Lessee name",
        )
    )

    # lessee_email
    fields.append(
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="lessee_email",
            display_name="Lessee email",
        )
    )

    template = client.metadata_templates.create_metadata_template(
        scope=scope,
        template_key=template_key,
        display_name=display_name,
        fields=fields,
        copy_instance_on_item_copy=True,
    )

    return template


def apply_metadata_to_document(
    client: BoxClient, file_id: str, template_key: str, data: Dict[str, str]
) -> MetadataFull:
    # remove empty values
    data = {k: v for k, v in data.items() if v}

    # Apply metadata to document
    try:
        return client.file_metadata.create_file_metadata_by_id(
            file_id=file_id,
            scope=CreateFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
            request_body=data,
        )
    except BoxAPIError as error_a:
        if error_a.response_info.status_code == 409:
            # Update the metadata
            update_data = []
            for key, value in data.items():
                update_item = UpdateFileMetadataByIdRequestBody(
                    op=UpdateFileMetadataByIdRequestBodyOpField.ADD,
                    path=f"/{key}",
                    value=value,
                )
                update_data.append(update_item)
            try:
                return client.file_metadata.update_file_metadata_by_id(
                    file_id=file_id,
                    scope=UpdateFileMetadataByIdScope.ENTERPRISE,
                    template_key=template_key,
                    request_body=update_data,
                )
            except BoxAPIError as error_b:
                raise error_b
        else:
            raise error_a


def get_metadata_from_document(
    client: BoxClient, file_id: str, template_key: str
) -> MetadataFull:
    """Get file metadata"""
    return client.file_metadata.get_file_metadata_by_id(
        file_id=file_id,
        scope=CreateFileMetadataByIdScope.ENTERPRISE,
        template_key=template_key,
    )
