import logging
import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status

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
    