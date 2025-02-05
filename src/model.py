
from pydantic import BaseModel

class my_file_model(BaseModel):    
    id: int
    source_file: str
    date: str   
    
