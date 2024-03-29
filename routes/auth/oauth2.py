from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer
)
from routes.auth import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return Token.verify_token(token, credentials_exception)


def get_current_doc_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return Token.verify_doc_token(token, credentials_exception)
