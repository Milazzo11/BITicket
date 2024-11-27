"""
"""


import time
import uuid
from config import DEFAULT_EVENT_TTL, DEFAULT_EVENT_TICKETS, DEFAULT_EXCHANGES
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Union

from app.crypto.symmetric import SKE

from fastapi import HTTPException

from .storage import event as event_db





class Data(BaseModel):
    event_key: bytes = Field(default_factory=SKE.key, description="Ticket granting master key for event")
    owner_public_key: str = Field(..., description="Public key of event creator")
    returned: List[int] = Field([], description="Returned (and not yet reissued) ticket numbers")


    @classmethod
    def from_dict(self, data: dict) -> "Data":
        instance = self()

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return instance


    def to_dict(self) -> dict:
        return self.__dict__
    

    def reissue_ticket(self) -> Optional[int]:
        """
        """

        if len(self.returned) != 0:
            return self.returned.pop()
        
        else:
            return None




class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Event ID")
    name: str = Field(..., description="Event name")
    description: str = Field(..., description="Event description")
    tickets: int = Field(DEFAULT_EVENT_TICKETS, description="Number of total event tickets")
    issued: int = Field(0, description="Number of tickets issued")
    start: float = Field(default_factory=lambda: time.time(), description="Epoch timestamp of event start date")
    end: float = Field(default_factory=lambda: time.time() + DEFAULT_EVENT_TTL, description="Epoch timestamp of event end date")
    exchanges: int = Field(DEFAULT_EXCHANGES, description="Maximum amount of user exchanges allowed for event tickets")
    private: bool = Field(False, description="Specifies whether event is public (open) or private (requires authorization)")
    # TODO - set contstriants on these values
    ## also: the select * always loading style into event doesn't seem sustainable



    @classmethod
    def from_dict(self, data: dict) -> "Event":
        instance = self()

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return instance




    @classmethod
    def load(self, event_id: str) -> "Event":
        """
        """
        
        dict = event_db.load(event_id)
        return self.from_dict(dict)






    def to_dict(self) -> dict:
        return self.__dict__



    def create(self, owner_public_key: str) -> str:
        """

        :return: event ID
        """

        event_data = Data(owner_public_key=owner_public_key)
        event_db.create(self.to_dict(), event_data.to_dict())


    def next_ticket(self) -> int:
        """
        """

        if self.issued >= self.tickets:
            raise HTTPException(status_code=401, detail="All tickets registered")
        
        self.issued += 1

        return self.issued - 1








class EventData(BaseModel):
    event: Event = Field(..., description="User-facing event packet")
    data: Data = Field(..., description="Event data")


    @classmethod
    def load(self, event_id: str) -> "EventData":
        """
        """

        dict = event_db.load_full(event_id)

        return self(
            event=Event.from_dict(dict["event"]),
            data=Data.from_dict(dict["data"])
        )
    

    @classmethod
    def from_dict(self, dict) -> "EventData":
        self.event = Event.from_dict(dict["event"])
        self.data = Data.from_dict(dict["data"])


    def to_dict(self) -> dict:
        return {
            "event": self.event.to_dict(),
            "data": self.event.to_dict()
        }
    

    def next_ticket(self) -> int:
        issue_num = self.data.reissue_ticket()

        if issue_num is None:
            issue_num = self.event.next_ticket()

        return issue_num





def search(text: str, limit: int) -> List[Event]:
    """
    """

    raw_data = event_db.search(text, limit)
    data_list = []

    for event_dict in raw_data:
        data_list.append(Event.from_dict(event_dict))

    return data_list