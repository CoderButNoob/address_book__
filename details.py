from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import get_type_hints
import re

class Details(BaseModel):
    first_name : str = Field(..., description="First Name of Contact")
    last_name : str = Field(default="", description="Last Name of Contact")
    address : str 
    city : str 
    state : str 
    zip_code : str 
    phone : str 
    email : EmailStr

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls , value):
        if not value.istitle():
            raise ValueError("First Name should start with a capital letter")
        return value    
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls , value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError("Zip Code must be 6 digit")
        return value
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls , value):
        import re
        phone_pattern = r"^\+[0-9]{2}\s[0-9]{10}"
        if not re.match(phone_pattern,value):
            raise ValueError("Phone Number must be in +91 1234456789 format")
        return value

    def __str__(self):
        return (
        f"First Name : {self.first_name}\n"
        f"Last Name : {self.last_name}\n"
        f"Address : {self.address}\n"
        f"City : {self.city}\n"
        f"State : {self.state}\n"
        f"Zip Code : {self.zip_code}\n"
        f"Phone : {self.phone}\n"
        f"Email : {self.email}"
        )
    
def get_contact_input():
    """
       Prompts the user to enter values for  each field 
       Returns a validated Detail
    """

    field_name = get_type_hints(Details).keys()
    input_data = {}

    input_data = {field: input(f"{field.replace('_','').title()}: ").strip() for field in field_name}

    try:
        return Details(**input_data)
    except Exception as e:
        print("vallidation Error", e)
        return None
    
        



