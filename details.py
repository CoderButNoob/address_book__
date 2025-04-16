from pydantic import BaseModel, Field, EmailStr, field_validator

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
    
    @field_validator('last_name')
    @classmethod
    def validate_first_name(cls , value):
        if not value.istitle():
            raise ValueError("Last Name should start with a capital letter")
        return value
    
    @field_validator('zip_code')
    @classmethod
    def validate_first_name(cls , value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError("Zip Code must be 6 digit")
        return value
    
    @field_validator('phone')
    @classmethod
    def validate_first_name(cls , value):
        import re
        phone_pattern = r"^\+[0-9]{2}\s[0-9]{7-9}"
        if not re.match(phone_pattern,value):
            raise ValueError("Phone Number must be in +91 1234456789 format")
        return value
    
    