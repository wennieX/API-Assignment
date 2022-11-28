from pydantic import BaseModel
# from typing import Optional, Union


# Model for validating post requests.
class InforData(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str
    country_code: str

