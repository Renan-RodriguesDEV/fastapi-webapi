import datetime

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.config.config import get_session
from database.models.user import User

# Algoritimo de hash do JWT
ALGORITHM = "HS256"
# Chave secreta para gerar o JWT
SECRET_KEY = "my-secret-key"
# Costante de tempo em minutos para o exp
ACCESS_TOKEN_EXPIRE_TIME = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_acess_token(data: dict, expire_delta: datetime.timedelta | None = None):
    """Cria um token de acesso (JWT)

    Args:
        data (dict): dicionario com as chaves sub
        expire_delta (datetime.timedelta | None, optional): tempo de exp do token em minutos timedelta. Defaults to None.
    """
    # copia o dicionario para não atualizar o obj original
    data_copy = data.copy()
    # definindo tempo de exp com tempo atual + timedelta em minutos
    expire = datetime.datetime.utcnow() + (
        expire_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    )
    data_copy.update({"exp": expire})
    # gerar o encode do token jwt a partir do data com nossa secret key e nosso algoritimo
    encoded_token = jwt.encode(
        payload=data_copy,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_token


# o Depends é uma injeção de dependencia ele chama a função e obtem seu valor
# Depends: "Antes de executar esta função, execute primeiro essa outra função e passe-me o resultado".
# O oauth2_schema é uma instância de OAuth2PasswordBearer que extrai o token do cabeçalho Authorization
def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_schema)
):
    """Obtém o usuário atual a partir do token JWT.

    Args:
        session (Session, optional): Sessão do banco de dados. Defaults to Depends(get_session).
        token (str, optional): Token JWT. Defaults to Depends(oauth2_schema).

    Raises:
        exception_unauthorized: Se a validação do token falhar.
        exception_unauthorized: Se o usuário não for encontrado.

    Returns:
        User: O usuário atual.
    """
    exception_unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # desencodando o token para ver se a assinatura é valida
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        # pegando o sub (username)
        username: str = payload.get("sub")
    except jwt.DecodeError:
        raise exception_unauthorized
        # busca o usuario e lança um erro se não encontrar
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise exception_unauthorized
    return user


def verify_password(clean_passwd: str, hash_passwd: str):
    return bcrypt.checkpw(
        password=clean_passwd.encode(), hashed_password=hash_passwd.encode()
    )


def hash_password(clean_passwd: str, rounds=12):
    return bcrypt.hashpw(clean_passwd.encode(), salt=bcrypt.gensalt(rounds)).decode()
