from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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
