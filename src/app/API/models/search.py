from pydantic import BaseModel, Field
from app.data.event import Event
from app.data import event
from typing import Optional, List

from enum import Enum




class Mode(Enum):
    ID = "id"
    TEXT = "text"


## <- models folder with lots of diff files?  maybe use __init__ to make * import all
####
## these functionality blobs should prob be sepaarted somehow

class SearchRequest(BaseModel):
    text: str = Field(..., description="The search text or keywords to find relevant events")
    limit: int = Field(1, description="The maximum number of results to return")
    mode: Mode = Field(Mode.ID, description='Search mode: "id" or "text"')




class SearchResponse(BaseModel):
    events: List[Event] = Field([], description="List of events matching search parameters")


    @classmethod
    def generate(self, request: SearchRequest) -> "SearchResponse":
        """
        """

        if request.mode == Mode.ID:
            self.events = [Event.load(request.text)]

        else:
            self.events = event.search(request.text, request.limit)

#####