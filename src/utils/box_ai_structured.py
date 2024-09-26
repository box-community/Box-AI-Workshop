from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass
class LeaseDocument:
    property_id: str
    property_type: str
    lease_start_date: date
    lease_end_date: date
    monthly_rent: float
    property_address: str
    lessee_name: str
    lessee_email: str
    lessor_name: str
    agreement_date: date
    agreement_term: str
    number_of_bedrooms: int


# Define an Enum for the field types
class FieldType(Enum):
    STRING = "string"
    FLOAT = "float"
    INTEGER = "integer"
    DATE = "date"
    MULTI_SELECT = "multiSelect"
    SINGLE_SELECT = "singleSelect"
