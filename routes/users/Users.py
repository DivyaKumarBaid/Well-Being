from fastapi import Depends, APIRouter, HTTPException, status
import config.database as database
import uuid
from routes.users.models import (
                     Pre_userdata, User, User_data)
from routes.login.models import (IntervalToken_inc, IntervalToken_ret)
import email_sender.email_verification as email_verification
import routes.auth.hashing as hashing
from routes.auth import Token
import os

router = APIRouter(tags=["Users"], prefix="/users")

@router.post('/create', status_code=201)
def create_user(inc_user: User):

    try:
        etoken = Token.create_email_token(data={"sub": inc_user.email})
        Users = Pre_userdata(user=inc_user.user, password=hashing.hash_pass(
            inc_user.password), email=inc_user.email, user_id=str(uuid.uuid4()), email_token=etoken)
        cursor2 = database.user_col.find_one({"email": inc_user.email})
        if cursor2:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        else:
            cursor1 = database.unverified_user.find_one(
                {"email": inc_user.email})
            if cursor1:
                cursor3 = database.unverified_user.delete_one(
                    {"email": inc_user.email})

            res = database.unverified_user.insert_one(dict(Users))

            email_verification.email(inc_user.email, False)
            if not res:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/email_verification/{token}", status_code=200)
def verify_user_email(token: str):
    # try:
    cursor = database.unverified_user.find_one({"email_token": token})
    isValid = Token.verify_email_token(token)
    if not cursor or isValid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    User = User_data(
        user=cursor['user'],
        email=cursor['email'],
        password=cursor['password'],
        user_id=cursor['user_id']
    )

    res = database.user_col.insert_one(dict(User))

    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    dele = database.unverified_user.delete_one({"email": cursor["email"]})
    if not dele:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.post("/user_verification", status_code=200)
def verify_user_token(rtoken: IntervalToken_inc):
    try:

        token = Token.verify_token_at_call(rtoken.refresh_token)
        if token == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return IntervalToken_ret(access_token=token)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
