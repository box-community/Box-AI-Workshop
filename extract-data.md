# Extract data (free form)

Sends an AI request to supported Large Language Models (LLMs) and extracts data in form of key-value pairs. Freeform ata extraction does not require any metadata template setup before sending the request.

Typically you would extract data from a single document, or at least from each document individually. The AI model will provide key-value pairs based on the content of the document(s).

Consider this sample code snippet:

```python
# Extract data from single document
prompt = f"Extract data from document {hab_files[0].name}"
items = [AiItemBase(id=hab_files[0].id, type="file")]
ai_response = client.ai.create_ai_extract(prompt=prompt, items=items)
print_ai_response(prompt, ai_response)
```

To extract data from a document, you need to specify:
 - prompt: What you want to extract from the document
 - items: A list of `AiItemBase` with a single Box file id

 The above example, in my case, returned:

```
Prompt: Extract data from document

Answer:
{"Lease Start Date": "5/1/24", "Lease End Date": "4/30/27", "Monthly Rent": "$3,125.00", "Lease Agreement Date": "4/24/24", "Lessor Name": "Schiaparelli plaza", "Lessor Address": "Schiaparelli crater, Oceanus Procellarum, Moon", "Lessee Name": "Marie Tharp", "Lessee Address": "marie.tharp@moonhabitat.space", "Property Description": "HAB-1-01, Sigle unit in Communal Dome of lunar surface, on the Schiaparelli Plaza Property", "Property Type": "Lunar Habitat Unit"}
```

As you can see even with a vague prompt, the AI model was able to extract key-value pairs from the document. 

We can however be more specific with the prompt, for example:

```python
prompt = (
        "Property id,"
        "Lease Start Date, Lease End Date, Monthly Rent, Property Address,"
        "Lessee Name, Lessee Email, Lessor Name, Agreement Date, "
        "Agreement Term, Number of bed rooms as an integer, "
        "all dates should be in format yyyy-mm-dd"
    )
items = [AiItemBase(id=hab_files[0].id, type="file")]
ai_response = client.ai.create_ai_extract(prompt=prompt, items=items)
...
```

Returns this:
```
Document 1:
Property id: HAB-1-01
Lease Start Date: 2024-05-01
Lease End Date: 2027-04-30
Monthly Rent: 3,125.00
Property Address: Schiaparelli Plaza Property
Lessee Name: Marie Tharp
Lessee Email: marie.tharp@moonhabitat.space
Lessor Name: Schiaparelli plaza
Agreement Date: 2024-04-24
Agreement Term: 3 years
Number of bed rooms: 1
```

Go ahead and execute the script `src/box_ai_extract.py` to see the data extraction process.

Take a look at the [workshop](src/box_ai_extract.py) script to see how to extract data from multiple documents.


