from pydantic import BaseModel, Field



class CurrencyGet(BaseModel):
    name: str = Field(max_length=3)

class CurrencyRead(BaseModel):
    name: str = Field(max_length=3)
    price:float

class CurrenciesRead(BaseModel):
    currencies: list

