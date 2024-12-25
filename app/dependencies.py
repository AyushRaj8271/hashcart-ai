from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, database,utils,roles
from app.database import get_db
# from app.utils import get_current_user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise credentials_exception
#     return user

# def get_current_active_user(current_user: models.User = Depends(get_current_user)):
#     if current_user.role not in [roles.Roles.ADMIN, roles.Roles.SHOPPER, roles.Roles.BUSINESS]:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user

# def get_access_permission(access: str):
#     def access_permission(current_user: models.User = Depends(get_current_active_user)):
#         if access not in roles.ROLE_ACCESS.get(current_user.role, []):
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#         return current_user
#     return access_permission


# 


# def get_role_access(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):




def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(utils.oauth2_scheme)):
    try:
        user_id = utils.decode_token(token)
        print("uuuuuuuuuuuu--->",user_id)
        user = db.query(models.User).filter(models.User.id == user_id).first()
        print("userr------",user.role)
        if user is None:
            print("user===",user)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    except Exception as e:
        print("sdfomsdf--------",e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials: {e}")

def get_role_access(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user_role = current_user.role
    print("get_role_Acess",user_role)
    return user_role

# def shopper_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
#     user_role = get_role_access(db, current_user)
#     if user_role != "shopper":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user

# def admin_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
#     user_role = get_role_access(db, current_user)
#     if user_role != "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user

# def business_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
#     user_role = get_role_access(db, current_user)
#     if user_role != "business":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
#     return current_user

def admin_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user_role = get_role_access(db, current_user)
    if user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

def shopper_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user_role = get_role_access(db, current_user)
    if user_role not in ["shopper", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

def business_access(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    user_role = get_role_access(db, current_user)
    if user_role not in ["business", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

