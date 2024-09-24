from typing import List

from box_sdk_gen import AiItemBase, AiResponse, BoxClient, CreateAiAskMode, File


def test_ai_ask_single_item(
    box_client_ccg_user: BoxClient, box_test_samples: List[File]
):
    client = box_client_ccg_user

    prompt = "Summarize document"
    item = AiItemBase(id=box_test_samples[0].id, type="file")
    ai_response: AiResponse = client.ai.create_ai_ask(
        mode=CreateAiAskMode.SINGLE_ITEM_QA,
        prompt=prompt,
        items=[item],
    )

    assert ai_response is not None


def test_ai_ask_multi_item(
    box_client_ccg_user: BoxClient, box_test_samples: List[File]
):
    client = box_client_ccg_user

    prompt = "Summarize documents"
    items = [AiItemBase(id=file.id, type="file") for file in box_test_samples]
    ai_response: AiResponse = client.ai.create_ai_ask(
        mode=CreateAiAskMode.MULTIPLE_ITEM_QA,
        prompt=prompt,
        items=items,
    )

    assert ai_response is not None
