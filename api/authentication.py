import typing
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import JWTError, jwt
from starlette import status

http_basic = HTTPBasic()


def basic_authentication(credentials: HTTPBasicCredentials = Depends(http_basic)):
    if credentials.username == "isfakiri" and credentials.password == "password123":
        return
    # 401 - invalid credentials, authorization failures
    # 403 - forbidden
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
    )


# Use https://jwt.io/
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.I1qJCUASlxuKvXx3BcooSig8TbGL6F5vkTH5s36-1oY


@dataclass
class Token:
    name: str
    admin: bool


def jwt_authentication(authorization: typing.Union[str, None] = Header(default=None)):
    token_secret = "isfakiri"
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    token = authorization.split(" ")[1]
    try:
        token_payload = jwt.decode(token=token, key=token_secret, algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        ) from e
    return Token(
        name=token_payload.get("name"), admin=token_payload.get("admin", False)
    )
