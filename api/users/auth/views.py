from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.users.manager import get_user_manager
from api.users.auth.backend import authentication_backend
from api.users.schemas import EmailPassword
from api.users.auth.transport import token_transport

router = APIRouter(prefix='/auth/token', tags=['Auth'])

@router.post('/login', response_model=dict)
async def login(
    request: EmailPassword,
    user_manager = Depends(get_user_manager),
    strategy = Depends(authentication_backend.get_strategy)
)-> dict:
    credentials = OAuth2PasswordRequestForm(
        username=request.email,
        password=request.password,
    )
    user = await user_manager.authenticate(credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный email или пароль')
    token = await strategy.write_token(user)
    return {
        'auth_token': token,
    }

@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: str = Depends(token_transport),
    strategy = Depends(authentication_backend.get_strategy),
    user_manager = Depends(get_user_manager)
)-> None:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await strategy.read_token(token, user_manager)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await strategy.destroy_token(token, user)
    return None