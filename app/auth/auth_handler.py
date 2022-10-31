import os
import time
import jwt

JWT_SECRET = os.getenv("secret")
JWT_ALGORITHM = os.getenv("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str):
    payload = {
        "user": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() and decoded_token["user"] == os.getenv("login") else None
    except Exception as e:
        return e
