from utils.box_client_ccg import AppConfig, get_ccg_user_client, whoami
from utils.box_metadata import create_leases_template, get_template_by_key


def main():
    # get box user client
    conf = AppConfig()
    print(f"\nConfiguration:\n{conf.to_dict()}")

    # get ccg user client
    print("\nGetting CCG user client..")
    client = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    user = whoami(client)
    print(f"Who am I: {user.name} (id: {user.id})")

    # create leases template
    template_key = "leases_workshop"
    template_display_name = "Leases Workshop"

    # template = get_template_by_key(client, template_key)
    # # force delete template
    # if template:
    #     print(
    #         f"\nMetadata template found: {template.display_name} ",
    #         f"[{template.id}]",
    #     )
    #     print("\nDeleting metadata template...")
    #     delete_template_by_key(client, template_key)
    #     print("\nMetadata template deleted.")

    template = get_template_by_key(client, template_key)

    if template:
        print(
            f"\nMetadata template found: {template.display_name} ",
            f"[{template.id}]",
        )
    else:
        print("\nMetadata template does not exist, creating...")
        # create a metadata template
        template = create_leases_template(client, template_key, template_display_name)
        print(
            f"\nMetadata template created: {template.display_name} ",
            f"[{template.id}]",
        )


if __name__ == "__main__":
    main()
