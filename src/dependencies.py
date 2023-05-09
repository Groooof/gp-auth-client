import typing as tp

from fastapi import Request, HTTPException, Depends
import aioredis

from src.redis import redis
from src import config


def get_redis_client():
    return redis


class SessionCookie:
    def __init__(self, name: str = config.USER_SESSION_COOKIE_NAME, raise_exc: bool = True) -> None:
        self._name = name
        self._raise_exc = raise_exc

    async def __call__(self,
                 request: Request,
                 redis: aioredis.Redis = Depends(get_redis_client)) -> tp.Union[tp.Optional[str], tp.Optional[str]]:
        session = request.cookies.get(self._name)  # http only
        
        if session is None:
            if self._raise_exc:
                raise HTTPException(status_code=400, detail='invalid_token')
            else:
                return None, None
            
        user_id = await redis.get(session)
        if user_id is None:
            if self._raise_exc:
                raise HTTPException(status_code=400, detail='invalid_token')
            else:
                return None, None
            
        return session, user_id

