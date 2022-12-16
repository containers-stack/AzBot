from pydantic import BaseModel

class Message(BaseModel):
    SubscriptionId: str
    Description: str