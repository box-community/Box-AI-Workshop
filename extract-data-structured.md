# Extract structured data

Sends an AI request to supported Large Language Models (LLMs) and returns extracted data as a set of key-value pairs. For this request, you need to define a schema yourself.

## Official documentation
- [Guide](https://developer.box.com/guides/box-ai/extract-metadata-structured/)
- [API reference](https://developer.box.com/reference/post-ai-extract-structured/)

## Workshop

Here is an example on how to define an element for the extraction schema:

```python
CreateAiExtractStructuredFields(
    type=FieldType.DATE,
    key="lease_start_date",
    prompt="Lease Start Date in YYYY-MM-DD format",
)
```

The `CreateAiExtractStructuredFields` class has the following parameters:
- `key`: str, the key of the extracted field
- `description`: Optional[str] = None, a description of the field
- `display_name`: Optional[str] = None, a display name for the field
- `prompt`: Optional[str] = None, a prompt for the field
- `type`: Optional[str] = None, the type of the field
- `options`: Optional[List[CreateAiExtractStructuredFieldsOptionsField]] = None, options for the field

The schema element serves 2 purposes:
- It defines the output key and format for the extracted data
- It provides a prompt for the AI model to understand what you are looking for

You can define multiple fields for the schema and then use it in the AI request:

```python
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
# ... many more fields ...

# Extract data from single document
ai_response: AiExtractResponse = client.ai.create_ai_extract_structured(
    items=[item], fields=fields
)
print_ai_response("Extract data from document", ai_response)
```

In my case, the above example returned:

```
Prompt: Extract data from document

Answer:
{'property_address': 'Schiaparelli Plaza Property', 'number_of_bedrooms': 1, 'lessee_email': 'marie.tharp@moonhabitat.space', 'lessee_name': 'Marie Tharp', 'agreement_date': '2024-04-24', 'lease_start_date': '2024-05-01', 'lease_end_date': '2027-04-30', 'monthly_rent': 3125, 'property_type': 'HAB-1', 'lessor_name': 'Schiaparelli plaza', 'agreement_term': 3, 'property_id': 'HAB-1-01'}
```

Go ahead and execute the script `src/box_ai_extract_structured.py` to see the data extraction process.

Take a look at the [workshop](src/box_ai_extract_structured.py) script to see how to extract data from multiple documents.
