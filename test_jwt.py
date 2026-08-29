from app.core.security import (
    create_access_token,
    decode_access_token,
)


token = create_access_token(
    {
        "sub": "1"
    }
)

print(f"TOKEN: {token}")


payload = decode_access_token(token)

print(f"\nPAYLOAD: {payload}")