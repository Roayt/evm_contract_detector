from fastapi.testclient import TestClient

from api import app, get_pool


class FakePool:
    async def fetchval(self,query):
        return 1

    async def fetch(self,query,*args):

        if "check_point" in query:
                  status={
                "chain": 11155111,
                "last_processed_block": 11725165,
                "updated_at": "2026-10-02T07:15:46.494994Z"
              }
                  return[status]
        else:
            contract={"id":1,"contract_address":"0x8e5ecb9a5e416722f41c1c8acec18965ae33e767",
                    "deployer_address":"0xfd36b412564060ea7a53c2c4a1afd78636880a41","chain":11155111,
                    "symbol":"TEST2","blocknumber":11725161,"created_at":"2026-09-17T17:25:14.458892Z"}

            return [contract]

    async def fetchrow(self,query,*args):
        return None

fake_pool=FakePool()

async def overide_get_pool():
    return fake_pool
app.dependency_overrides[get_pool]=overide_get_pool

client=TestClient(app)

def test_health_check():
    response=client.get("/api/health")
    assert response.status_code==200
    assert response.json()=={"status":"healthy"}

def test_checkPoint_status():
    response=client.get("/api/status")
    assert response.status_code==200
    assert response.json()==[{
    "chain": 11155111,
    "last_processed_block": 11725165,
    "updated_at": "2026-10-02T07:15:46.494994Z"
  }]

def test_contract_detail():
     response=client.get("/api/contracts")
     assert response.status_code==200
     assert response.json()==[{
    "id": 1,
    "deployer_address": "0xfd36b412564060ea7a53c2c4a1afd78636880a41",
    "contract_address": "0x8e5ecb9a5e416722f41c1c8acec18965ae33e767",
    "chain": 11155111,
    "symbol": "TEST2",
    "blocknumber": 11725161,
    "created_at": "2026-09-17T17:25:14.458892Z"
  }]
def test_specific_contract():
     response=client.get("/api/contracts/0x8e5ecb9a5e416722f41c1c8acec18965ae33e767")
     assert response.status_code==200
     assert response.json()==[{
    "id": 1,
    "deployer_address": "0xfd36b412564060ea7a53c2c4a1afd78636880a41",
    "contract_address": "0x8e5ecb9a5e416722f41c1c8acec18965ae33e767",
    "chain": 11155111,
    "symbol": "TEST2",
    "blocknumber": 11725161,
    "created_at": "2026-09-17T17:25:14.458892Z"
  }]
