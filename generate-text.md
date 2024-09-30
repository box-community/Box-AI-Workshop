# Generate text

You can use Box AI to generate text based on provided content, and then use the generated text to create new content. The difference between Generate text and Ask endpoints, is that the Generate text endpoint accepts the dialog history as input, allowing your user to build upon the generated text.


## Official documentation
- [Guide](https://developer.box.com/guides/box-ai/generate-text/)
- [API reference](https://developer.box.com/reference/post-ai-text-gen/)

## Workshop

To generate text, you need to specify:
 - `prompt`: What you want to generate text for
 - `items`: A list of `AiItemBase` with a single Box file id
 - `content`: The content you want to generate text for
 - `dialogue_history`: A list of `AiDialogueHistory` that represent the dialog history

Consider this sample code snippet:

```python
# Text Generation accepts a single file, and uses it exclusively
# to check if the user has permissions to use Box AI
# It does accept context as a starting point/topic
item = CreateAiTextGenItems(
    id=hab_files[0].id, type="file", content="Leasing properties on the moon"
)
dialog_history: List[AiDialogueHistory] = []

# Infinite cycle to ask the user for prompts
while True:
    # Ask user for prompt
    prompt = input("\nWhat would you like to talk about?, 'q' to quit): ")

    if prompt == "q":
        break

    # AI Ask Text Generation
    ai_response: AiResponseFull = client.ai.create_ai_text_gen(
        prompt=prompt,
        items=[item],
        dialogue_history=dialog_history,  # if dialog_history else None,
    )
    print_ai_response(prompt, ai_response)
    dialog_history.append(
        AiDialogueHistory(
            prompt=prompt,
            answer=ai_response.answer,
            created_at=ai_response.created_at,
        )
    )
```

In the example above, we keep building the dialog history, so that the AI does not loose context. This is useful when you want to generate text based on a conversation, or a series of prompts.

Here are some examples:

```
What would you like to talk about?, ('q' to quit): tell me about it

================================================================================
Prompt: tell me about it
--------------------------------------------------------------------------------
Answer:
Leasing properties on the moon is an exciting concept that has gained attention in recent years. As space exploration and commercialization continue to advance, the idea of owning or leasing land on celestial bodies like the moon has become a topic of interest.

...

While it may be some time before leasing properties on the moon becomes a reality, it is an intriguing possibility that could open up new opportunities for human exploration and utilization of space resources.
================================================================================
```
Notice how the AI started discussing leases despite the vague prompt, as it got that information from the content.

Continuing the conversation:
```
What would you like to talk about?, 'q' to quit): what would be a good mix of offerings

================================================================================
Prompt: what would be a good mix of offerings
--------------------------------------------------------------------------------
Answer:
A good mix of offerings for leasing properties on the moon could include:

1. Lunar Research Stations: Providing facilities for scientific research and experimentation in a unique lunar environment.

2. Tourism Outposts: Offering accommodations and experiences for tourists looking to visit the moon for leisure or educational purposes.

3. Mining Operations: Leasing areas for companies interested in extracting resources from the moon, such as water ice or rare minerals.

4. Communication Infrastructure: Establishing communication relay stations on the moon to support space missions and satellite operations.

5. Sustainable Living Spaces: Developing habitats that prioritize sustainability and self-sufficiency, potentially serving as models for future space colonization efforts.

6. Educational Programs: Creating opportunities for schools, universities, and research institutions to conduct educational programs and workshops on the moon.

By offering a diverse range of services and facilities, leasing properties on the moon can cater to various industries and interests while promoting innovation and collaboration in space exploration endeavors.
================================================================================
```

As you can see, because we are sending back the dialog history, the AI is able to stay on topic.

Go ahead and execute the script `src/box_ai_text_gen.py` to see the data extraction process.

Take a look at the [workshop](src/box_ai_text_gen.py) script to see how this was implemented.
