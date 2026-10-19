"""HTTP interface for artificial-funds research sandbox."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app import core


@asynccontextmanager
async def lifespan(app: FastAPI):
    core.initialize()
    yield


app = FastAPI(title="Financial Mixer Lab", version="0.1.0", lifespan=lifespan)


class AccountIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    currency: str = "RUB"
    opening_balance: int = Field(default=0, ge=0)


class PaymentIn(BaseModel):
    from_account: int
    to_account: int
    amount: int = Field(gt=0)
    idempotency_key: str = Field(min_length=1, max_length=128)


def respond(fn, *args):
    try:
        return fn(*args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
def health():
    return {"status": "ok", "environment": "simulated"}


@app.post("/accounts", status_code=201)
def create_account(payload: AccountIn):
    return respond(core.create_account, payload.name, payload.currency,
                   payload.opening_balance)


@app.get("/accounts/{account_id}")
def account(account_id: int):
    return respond(core.get_account, account_id)


@app.post("/transfers", status_code=201)
def payment(payload: PaymentIn):
    return respond(core.transfer, payload.from_account, payload.to_account,
                   payload.amount, payload.idempotency_key)


@app.get("/transfers/{transfer_id}")
def payment_detail(transfer_id: int):
    return respond(core.get_transfer, transfer_id)


@app.get("/ledger/{account_id}")
def entries(account_id: int):
    return respond(core.ledger, account_id)


@app.get("/audit")
def audit():
    return {"unbalanced_transfer_ids": core.validate_journal()}
