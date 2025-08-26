from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.config.config import get_session
from database.models.user import User
from database.schemas.token import Token
from security.auth import create_acess_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


# o form_data add nos headers do cliente o bearer token
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # o depends resolve o problema do form_data
    session: Session = Depends(get_session),
):
    # pega o usuario e verifica se existe
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
        )
    # checa se a senha está correta
    if not verify_password(form_data.password, user.password):
        print(form_data.password, user.password)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    # gera o token de acesso
    access_token = create_acess_token({"sub": user.username})
    # isso add nos headers do cliente o bearer token
    return {"access_token": access_token, "token_type": "bearer"}
