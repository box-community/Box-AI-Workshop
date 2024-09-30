from typing import List

from box_sdk_gen import (
    AiDialogueHistory,
    AiResponseFull,
    BoxClient,
    CreateAiTextGenItems,
)

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
    hab_files = files_start_with("HAB-2", client, conf)

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
        prompt = input("\nWhat would you like to talk about?, ('q' to quit): ")

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


if __name__ == "__main__":
    main()
