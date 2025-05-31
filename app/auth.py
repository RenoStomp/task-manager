from fastapi import Header, HTTPException, status

# "захардкоденный секретный токен"
API_TOKEN = "hardcoded-secret-token"

# проверяем токен и либо проходим дальше, либо возвращаем код ошибки с комментом
def get_token_header(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token")
