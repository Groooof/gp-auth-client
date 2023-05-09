import pydantic as pd


class Callback:
    class Request:
        class Query(pd.BaseModel):
            code: str
            state: str
