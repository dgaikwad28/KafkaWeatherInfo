from pydantic import BaseModel


class UserLocationEvent(BaseModel):
    userID: str
    latitude: str
    longitude: str
