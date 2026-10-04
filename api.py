import datetime
import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

import asyncpg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = os.getenv("DATABASE_API_URL")
    if not db:
        raise ValueError("DATABASE_API_URL not found")
    result = await asyncpg.create_pool(db)
    app.state.pool = result
    pool = app.state.pool

    yield
    await pool.close()


app = FastAPI(lifespan=lifespan)


async def get_pool(request: Request):
    pool = request.app.state.pool
    return pool


@app.get("/api/health")
async def db_pool_health_check(db: asyncpg.Pool = Depends(get_pool)):  # noqa: B008
    try:
        await db.fetchval("SELECT 1")
        return {"status": "healthy"}

    except Exception as e:
        logger.exception("health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="health check not succeeded",
        ) from e


class Status(BaseModel):
    chain: int
    last_processed_block: int
    updated_at: datetime.datetime


@app.get("/api/status", response_model=list[Status])
async def checkPoint_status(db: asyncpg.Pool = Depends(get_pool)):
    result = await db.fetch(
        "SELECT chain, last_processed_block,updated_at FROM check_point ORDER BY chain"
    )
    check_point = []
    for row in result:
        check_point.append(dict(row))

    return check_point


class Contract(BaseModel):
    id: int
    deployer_address: str
    contract_address: str
    chain: int
    symbol: str
    blocknumber: int
    created_at: datetime.datetime

 
@app.get("/api/contracts", response_model=list[Contract])
async def get_contract_detail(
    symbol: str | None = None,
    chain: int | None = None,
    limit: Annotated[int, Query(le=200, ge=1)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: asyncpg.Pool = Depends(get_pool),
):

    result = await db.fetch(
        "SELECT id, contract_address, chain, symbol, blocknumber, created_at , deployer_address FROM contract WHERE($1::text IS NULL OR lower(symbol)=lower($1)) AND ($2::integer IS NULL OR chain=$2) ORDER BY id DESC LIMIT $3 OFFSET $4",
        symbol,
        chain,
        limit,
        offset,
    )

    contract_status = []
    for row in result:
        contract_status.append(dict(row))

    return contract_status


@app.get("api/contracts/{contract_address}", response_model=list[Contract])
async def get_specific_contract(
    contract_address: str = Path(pattern="^0x[0-9a-fA-F]{40}$"),
    db: asyncpg.Pool = Depends(get_pool),
):
    contract_address = contract_address.lower()

    result = await db.fetch(
        "SELECT id, contract_address, chain, symbol, blocknumber, created_at , deployer_address FROM contract WHERE contract_address=$1 ORDER BY chain",
        contract_address,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contract address not found"
        )

    contracts = []
    for row in result:
        contracts.append(dict(row))
    return contracts
