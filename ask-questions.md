# Ask questions

Sends an AI request to supported LLMs and returns an answer specifically focused on the user's question given the provided context.

You can ask questions about a single document or multiple documents. The AI model will provide an answer based on the context of the question and the content of the document(s).

## Official documentation
- [Guide](https://developer.box.com/guides/box-ai/ask-questions/)
- [API reference](https://developer.box.com/reference/post-ai-ask/)


## Ask questions about a single document

Consider this code snippet:

```python
# AI Ask single Summarize document
prompt = "Summarize document"
item = AiItemBase(id=hab_files[0].id, type="file")
ai_response: AiResponseFull = client.ai.create_ai_ask(
    mode=CreateAiAskMode.SINGLE_ITEM_QA,
    prompt=prompt,
    items=[item],
)
print(ai_response)
```

To get an answer to a question about a single document, you need to specify:
 - mode: `CreateAiAskMode.SINGLE_ITEM_QA`
 - prompt: The question you want to ask
 - items: A list of `AiItemBase` with a single Box file id

 The example above, in my case, returned:

 ```
Prompt: Summarize document

Answer:
The document is a Lunar Property Lease Agreement between Schiaparelli Plaza (Lessor) and Marie Tharp (Lessee), effective from May 1, 2024, to April 30, 2027. It outlines the lease of a lunar habitat unit (HAB-1-01) featuring a private bedroom, open-plan kitchen and living room, recycling facilities, life support systems, and high-bandwidth connectivity. The monthly rent is $3,125, due on the first of each lunar month. The agreement emphasizes compliance with international space laws, responsibilities for maintenance, insurance requirements, and conditions for termination. Disputes will be resolved through arbitration by the United Nations Office for Outer Space Affairs.
```

Go ahead and execute the script `src/box_ai_ask_single.py` to see the answer to your question about the document. We've included a few sample prompts, and you can also ask anything you want about the document.

```
Example prompts:
1. How many bedrooms does this unit has?
2. When should I send a contract renewal notification?
3. What is the annual rent for this unit?
4. Can the tenant work from home?
5. Are pets allowed?

Enter a prompt (or choose 1-5 from examples, 'q' to quit):
```

Take a look at the [workshop](src/box_ai_ask_single.py) script to see how to ask questions about a single document.

Simple, right?

## Ask questions about multiple documents

What if I want to provide the AI with more context over multiple documents? You can do that too, by providing a list of `AiItemBase` with multiple Box file ids.

Consider this code snippet:

```python
# AI Ask multi Summarize document
items = [AiItemBase(id=file.id, type="file") for file in hab_files]
prompt = "Which 5 contracts renew first?"
ai_response: AiResponseFull = client.ai.create_ai_ask(
    mode=CreateAiAskMode.MULTIPLE_ITEM_QA,
    prompt=prompt,
    items=items,
)
print_ai_response(prompt, ai_response)
```

To get an answer to a question about multiple documents, you need to specify:
 - mode: `CreateAiAskMode.MULTIPLE_ITEM_QA`
 - prompt: The question you want to ask
 - items: A list of `AiItemBase` with multiple Box file ids

The example above, in my case, returned:
```
Prompt: Which 5 contracts renew first?

Answer:
Now, let's identify the five contracts that renew first based on their end dates:

...

Thus, the five contracts that renew first are:
1. HAB-1-03
2. HAB-1-04
3. HAB-1-06
4. HAB-1-07
5. HAB-1-08
```

Go ahead and execute the script `src/box_ai_ask_multi.py`. We've included a few sample prompts, and you can also ask anything you want about the documents.

```
Example prompts:
1. What type of units are these?
2. Which 5 contracts renew first?
3. What is the monthly expected revenue for these units?

Enter a prompt (or choose 1-3 from examples, 'q' to quit):
```

Take a look at the [workshop](src/box_ai_ask_multi.py) script to see how to ask questions in the context of multiple documents.