import pandas as pd
from mailmerge import MailMerge
from utils.box_client_ccg import ConfigCCG


def test_file_csv_read(box_env_ccg):
    df = pd.read_csv(box_env_ccg.file_csv, sep=",", quotechar='"')
    assert df is not None
    assert len(df) > 0
    assert len(df.columns) > 0


def test_file_template_read(box_env_ccg: ConfigCCG):
    merge_doc = MailMerge(box_env_ccg.file_template)
    assert merge_doc is not None
    # print(merge_doc.get_merge_fields())
    assert len(merge_doc.get_merge_fields()) > 0


def test_file_merge(box_env_ccg: ConfigCCG):
    df = pd.read_csv(box_env_ccg.file_csv, sep=",", quotechar='"')
    merge_doc = MailMerge(box_env_ccg.file_template)
    fields = merge_doc.get_merge_fields()

    # sample row
    # {
    #     "Tenant": "Albert Einstein",
    #     "Email": "albert.einstein@moonhabitat.space",
    #     "Lease Date": "3/23/24",
    #     "Start Date": "4/1/24",
    #     "End Date": "3/31/27",
    #     "Property": "HAB-2-01",
    #     "Property Type": "Dual Residential Pod",
    #     "Property Description": "Two private and spacious bedrooms, each equipped with a temperature-regulating system, offering breathtaking views of the lunar landscape through reinforced transparent panels. Bedrooms are fitted with built-in storage for personal items and lunar suits.",
    #     "Bed rooms": 2,
    #     "Rent": 5535,
    # }

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
        out_file = f"{box_env_ccg.folder_samples}/{row.get('Property')}.docx"
        with open(out_file, "wb") as f:
            merge_doc.write(f)

        break
