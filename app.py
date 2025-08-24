import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.config.config import get_session
from database.models.user import User
from database.schemas.token import Token
from routes.auth import create_acess_token, verify_password
from routes.users import router as user_router

app = FastAPI(
    title="My Bullet API",
    description="that API development with python",
    version="1.0.0",
)
app.include_router(user_router)


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status": status.HTTP_200_OK, "message": "Hellow world!"}


# o form_data add nos headers do cliente o bearer token
@app.post("/token", response_model=Token)
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


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
