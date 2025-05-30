from fastapi import Header, HTTPException, status

API_TOKEN = "hardcoded-secret-token"

def get_token_header(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
