"""
API endpoints
"""

from app.API import API
from app.API.models import *
from fastapi import FastAPI


app = FastAPI()


@app.post("/search", description="Search for events")
async def search_events(data: Auth[SearchRequest]) -> Auth[SearchResponse]:
    return API.search_events(data)


@app.post("/create", description="Create a new event on the server")
async def create_event(data: Auth[CreateRequest]) -> Auth[CreateResponse]:
    return API.create_event(data)


@app.post("/register", description="Register a user for an event and return his ticket")
async def register_user(data: Auth[RegisterRequest]) -> Auth[RegisterResponse]:
    return API.register_user(data)


@app.post("/cancel", description="Cancel event registration (return ticket)")
async def cancel_ticket(data: Auth[CancelRequest]) -> Auth[CancelResponse]:
    return API.cancel_ticket(data)


@app.post(
    "/transfer",
    description="Return a ticket back to the server or transfer it to another user",
)
async def transfer_ticket(data: Auth[TransferRequest]) -> Auth[TransferResponse]:
    return API.transfer_ticket(data)


@app.post("/redeem", description="Redeem a ticket")
async def redeem_ticket(data: Auth[RedeemRequest]) -> Auth[RedeemResponse]:
    return API.redeem_ticket(data)


@app.post(
    "/verify",
    description="Verify (as an event owner) that a user has redeemed his ticket",
)
async def verify_redemption(data: Auth[VerifyRequest]) -> Auth[VerifyResponse]:
    return API.verify_redemption(data)
