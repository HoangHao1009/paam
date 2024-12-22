from fastapi import HTTPException, status

from app.core.app_config import settings
from app.engine import Survey

from redis import StrictRedis, RedisError
from typing import Dict, Optional, Any
import json

class RedisCacheDB:
    def __init__(self, host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True):
        try:
            self.client = StrictRedis(host=host, port=port, db=db, decode_responses=decode_responses)
        except RedisError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Redis service unavailable: {str(e)}"
            )
        
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except RedisError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Redis error occurred while fetching data: {str(e)}"
            )
    
    def set(self, key: str, value: Dict[str, Any], ttl: Optional[int]=3600):
        try:
            self.client.setex(key, ttl, json.dumps(value))
        except RedisError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Redis error occurred while setting data: {str(e)}"
            )

    def delete(self, key: str):
        self.client.delete(key)
        
    def exists(self, key: str) -> bool:
        return self.client.exists(key)
    
    def refresh(self, key: str, ttl: Optional[int]=3600):
        if self.exists(key):
            self.client.expire(key, ttl)
            
    def get_survey(self) -> Survey:
        survey_data = self.get('survey_data')
        return Survey(data=survey_data)
        
def get_redisdb() -> RedisCacheDB:
    redis_db = RedisCacheDB()
    return redis_db