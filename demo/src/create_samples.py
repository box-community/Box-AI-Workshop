import pandas as pd
from mailmerge import MailMerge
from utils.box_client_ccg import ConfigCCG


def execute_mail_merge():
    conf = ConfigCCG()

    df = pd.read_csv(conf.file_csv, sep=",", quotechar='"')
    merge_doc = MailMerge(conf.file_template)
    fields = merge_doc.get_merge_fields()
    print(f"{fields}\n")

    for row in df.to_dict(orient="records"):
        print(f"{row}\n")
        merge_doc.merge(
            Tenant=row.get("Tenant"),
            Email=row.get("Email"),
            Lease_Date=row.get("Lease Date"),
            Start_Date=row.get("Start Date"),
            End_Date=row.get("End Date"),
            Property=row.get("Property"),
            Property_Type=row.get("Property Type"),
            Property_Description=row.get("Property Description"),
            Bed_rooms=row.get("Bed rooms"),
            Rent=row.get("Rent"),
        )
        out_file = f"{conf.folder_samples}/{row.get('Property')}.docx"
        with open(out_file, "wb") as f:
            merge_doc.write(f)

        break


def main():
    execute_mail_merge()


if __name__ == "__main__":
    main()
