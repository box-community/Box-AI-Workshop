from pathlib import Path

import pandas as pd
from docxtpl import DocxTemplate
from utils.box_client_ccg import AppConfig


def test_file_csv_read(box_env_ccg):
    df = pd.read_csv(box_env_ccg.file_csv, sep=",", quotechar='"')
    assert df is not None
    assert len(df) > 0
    assert len(df.columns) > 0


def test_file_template_read(box_env_ccg: AppConfig):
    merge_doc = DocxTemplate(box_env_ccg.file_template)
    assert merge_doc is not None


def test_file_merge(box_env_ccg: AppConfig):
    df = pd.read_csv(box_env_ccg.file_csv, sep=",", quotechar='"')
    assert df is not None
    assert len(df) > 0
    assert len(df.columns) > 0

    doc = DocxTemplate(box_env_ccg.file_template)
    assert doc is not None

    for row in df.to_dict(orient="records"):
        context = {
            "Tenant": row.get("Tenant"),
            "Email": row.get("Email"),
            "LeaseDate": row.get("LeaseDate"),
            "StartDate": row.get("StartDate"),
            "EndDate": row.get("EndDate"),
            "Property": row.get("Property"),
            "PropertyType": row.get("PropertyType"),
            "Description": row.get("Description"),
            "BedRooms": row.get("BedRooms"),
            "Rent": f"${row.get("Rent"):,.2f}",
        }
        doc.render(context)
        assert doc.is_rendered
        # make sure folder samples exists and create if not
        Path(box_env_ccg.folder_samples).mkdir(parents=True, exist_ok=True)
        # save docx file
        doc_file_path = f"{box_env_ccg.folder_samples}/test_{row.get('Property')}.docx"
        doc.save(doc_file_path)
        assert doc.is_saved
        # check if file exists
        assert Path(doc_file_path).exists()
        # delete docx file
        Path(doc_file_path).unlink()
        # check tha file was deleted
        assert not Path(doc_file_path).exists()

        break
