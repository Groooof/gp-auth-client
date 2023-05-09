from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import RedirectResponse
import aioredis
import requests

from src.dependencies import get_redis_client, SessionCookie
from src.utils.crypto import generate_random_string
from src.auth import schemas as sch
from src import config
from src.utils import crypto


router = APIRouter()


@router.get('/login')
def login(response: Response):
    
    response_type = 'code'
    client_id = config.CLIENT_ID
    state = crypto.generate_random_string(config.STATE_LEN)
    nonce = crypto.generate_random_string(config.NONCE_LEN)
    redirect_uri = config.BASE_URL + config.CALLBACK_ROUTE
    
    url_query_params = f'?response_type={response_type}&client_id={client_id}&state={state}&nonce={nonce}&redirect_uri={redirect_uri}'
    url = config.GPAUTH_SERVICE_BASE_URL + config.GPAUTH_SERVICE_AUTHORIZE_ROUTE + url_query_params
    
    response = RedirectResponse(url=url, status_code=302)
    response.set_cookie('state', 
                        state,
                        max_age=5*60,
                        secure=True,
                        httponly=True,
                        samesite='none')
    response.set_cookie('nonce', 
                        nonce,
                        max_age=5*60,
                        secure=True,
                        httponly=True,
                        samesite='none')
    return response


@router.post('/logout')
async def logout(response: Response,
                 redis: aioredis.Redis = Depends(get_redis_client),
                 session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    await redis.delete(session)
    response.delete_cookie(config.USER_SESSION_COOKIE_NAME)
    response.status_code = 200
