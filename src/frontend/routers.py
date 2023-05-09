import json

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.dependencies import SessionCookie

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import RedirectResponse
import aioredis
import requests

from src.dependencies import get_redis_client
from src.utils.crypto import generate_random_string
from src.auth import schemas as sch
from src import config
from src.utils import crypto


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/')
async def get_main_page(request: Request,
                        session_data: str = Depends(SessionCookie(raise_exc=False))):
    
    print(request.url_for('callback'))
    
    session, user_id = session_data
    if session is not None:
        return RedirectResponse('/protected', status_code=302)

    return templates.TemplateResponse('main.html', {'request': request})


@router.get('/protected', tags=['internal_auth'])
async def get_protected_page(request: Request, 
                             session_data: str = Depends(SessionCookie(raise_exc=False))):
    
    session, user_id = session_data
    print(10*'*', session_data)
    if session is None:
        return RedirectResponse('/', status_code=302)
    
    return templates.TemplateResponse("protected.html", {"request": request, "user": user_id})


@router.get('/callback')
async def callback(response: Response,
                   request: Request,
                   query: sch.Callback.Request.Query = Depends(sch.Callback.Request.Query),
                   redis: aioredis.Redis = Depends(get_redis_client)):
    
    stored_state = request.cookies.get('state')
    recieved_state = query.state
    
    if recieved_state != stored_state:
        return RedirectResponse(url='/', status_code=302)
        # raise HTTPException(status_code=400, detail='invalid_request')
    
    code = query.code
    data = {
        "client_secret": config.CLIENT_SECRET,
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.BASE_URL + config.CALLBACK_ROUTE,
        "grant_type": "authorization_code",
        "code": code
    }
    token_url = config.GPAUTH_SERVICE_BASE_URL + config.GPAUTH_SERVICE_TOKEN_ROUTE
    resp = requests.post(token_url, data=json.dumps(data))
    if resp.status_code != 200:
        return RedirectResponse(url='/', status_code=302)
        # raise HTTPException(status_code=400, detail='invalid_request')
    
    resp_json = resp.json()
    stored_nonce = request.cookies.get('nonce')
    recieved_nonce = resp_json['nonce']
    
    if recieved_nonce != stored_nonce:
        return RedirectResponse(url='/', status_code=302)
        # raise HTTPException(status_code=400, detail='invalid_request')
    
    user_id = resp_json['user_id']

    session = generate_random_string(config.USER_SESSION_LEN)
    await redis.set(session, str(user_id), ex=int(config.USER_SESSION_LIFETIME.total_seconds()))
    response.set_cookie(config.USER_SESSION_COOKIE_NAME, 
                        session,
                        max_age=int(config.USER_SESSION_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True)

    return {'redirect_to': 'http://localhost:8001/protected'}
