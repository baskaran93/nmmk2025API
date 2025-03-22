from fastapi import FastAPI, HTTPException, Depends, APIRouter
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import datetime
from src.models.user import User, UserCreate, UserCheckIn, UserRegister, UserLogin, GetUserId, VerifyUserId
from src.db.database import get_db
from src.utils import token_generator
from src.utils.token_generator import require_auth

Base = declarative_base()


load_dotenv()
router = APIRouter()



@router.post("/user/login/")
def login_user(user_register: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserLogin).filter(UserLogin.username == user_register.username
                                          and UserLogin.password_hash == user_register.password_hash).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Username, password is incorrect, "
                                                    "please retry or register as a new user")
    access_token = token_generator.create_access_token(
        data={"sub": existing_user.username, "user_id": existing_user.id},
        expires_delta=datetime.timedelta(hours=1)
    )
    return {"message": "User Logged in Successfully", "access_token":access_token}



@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists by phone
    existing_user = db.query(User).filter(User.phone == user.phone).first()  # ✅ FIXED
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        registration_time=datetime.datetime.utcnow(),
        address=user.address,
        pincode=user.pincode
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


# User Check-in API
@router.post("/checkin/")
def check_in_user(user_check: UserCheckIn, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    if not user_check.id and not user_check.phone:
        raise HTTPException(status_code=400, detail="Either ID or phone number should be provided")

    user = None
    if user_check.id:
        user = db.query(User).filter(User.id == user_check.id).first()
    if not user and user_check.phone:
        user = db.query(User).filter(User.phone == user_check.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update check-in time
    user.checked_in_time = datetime.datetime.utcnow()
    user.is_checked_in = True
    db.commit()

    return {"message": "User checked in successfully", "checked_in_at": user.checked_in_time}

# User Check-in for Food API
@router.post("/foodcheckin/")
def food_check_in_user(user_check: UserCheckIn, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    if not user_check.id and not user_check.phone:
        raise HTTPException(status_code=400, detail="Either ID or phone number should be provided")

    user = None
    if user_check.id:
        user = db.query(User).filter(User.id == user_check.id).first()
    if not user and user_check.phone:
        user = db.query(User).filter(User.phone == user_check.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update food check-in time
    user.food_checked_in_time = datetime.datetime.utcnow()
    user.is_food_checked_in = True
    db.commit()

    return {"message": "User checked in at the food counter successfully", "checked_in_at": user.food_checked_in_time}

@router.get("/user/details/")
def get_all_user_details(db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"users": users}


@router.get("/getUserId/")
def get_user_id(user_id: GetUserId, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == user_id.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"user_id": user.id}


@router.get("/verifyUser/")
def verify_user(user_phone: VerifyUserId, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_phone.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"user_id": user.id}

