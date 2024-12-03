from pydantic import BaseModel, Field
from app.data.event import Event
from app.data import event
from typing import Optional, List

from enum import Enum



## <- models folder with lots of diff files?  maybe use __init__ to make * import all
####
## these functionality blobs should prob be sepaarted somehow

class SearchRequest(BaseModel):
    text: str = Field(..., description="The search text or keywords to find relevant events")
    limit: int = Field(1, description="The maximum number of results to return")
    mode: str = Field("id", description='Search mode: "id" or "text"')

    def to_dict(self) -> dict:
        return self.__dict__




class SearchResponse(BaseModel):
    events: List[Event] = Field([], description="List of events matching search parameters")


    @classmethod
    def generate(self, request: SearchRequest) -> "SearchResponse":
        """
        """

        print("ss")

        if request.mode.lower() == "id":
            events = [Event.load(request.text)]

        else:
            events = event.search(request.text, request.limit)

        print("fs")
        return self(events=events)
    

    def to_dict(self) -> dict:
        return {
            "events": [event.to_dict() for event in self.events]
        }