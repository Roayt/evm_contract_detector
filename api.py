import datetime
import logging
import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app:FastAPI):
    db=os.getenv("DATABASE_API_URL")
    if not db:
        raise ValueError("DATABASE_API_URL not found")
    result= await asyncpg.create_pool(db)
    app.state.pool=result
    pool=app.state.pool

    yield 
    await pool.close()
    
app=FastAPI(lifespan=lifespan)

async def get_pool(request:Request):
    pool=request.app.state.pool
    return pool

@app.get("/health")
async def db_pool_health_check(db:asyncpg.Pool=Depends(get_pool)):  # noqa: B008
    try:
        await db.fetchval("SELECT 1")
        return {"status":"healthy"}

    except Exception as e: 
        logger.exception("health check failed")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="health check not succeeded") from e


class Status(BaseModel):
    chain:int
    last_processed_block:int 
    updated_at: datetime.datetime

@app.get("/status", response_model= list[Status])
async def check_Point_status(db:asyncpg.Pool=Depends(get_pool)):
    result= await db.fetch('SELECT chain, last_processed_block,updated_at FROM check_point ORDER BY chain')
    check_point=[]
    for row in result:
        check_point.append(dict(row))


    return check_point