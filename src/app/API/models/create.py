from pydantic import BaseModel, Field
from app.data.event import Event
from typing import List, Optional



class CreateRequest(BaseModel):
    event: Event = Field(..., description="New event to create on server")


class CreateResponse(BaseModel):
    event_id: Optional[str] = Field(None, description="New event ID (if successfully created)")

    @classmethod
    def generate(self, request: CreateRequest, public_key: str) -> "CreateResponse":
        """
        """

        self.event_id = request.event.create(public_key)