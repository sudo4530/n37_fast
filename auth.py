from database import session, ENGINE
from models import User
from fastapi import HTTPException, status, Response, APIRouter, Depends
from werkzeug import security
from schemas import RegisterModel, LoginModel
from fastapi.encoders import jsonable_encoder

# access_security = JwtAccessBearer(secret_key=os.getenv("secret_key"), auto_error=True)

session = session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")

@auth_router.get("/")
async def auth():

    return {
        "message": "This is auth page"
    }

@auth_router.get("/login")
async def login():
    return {
        "message": "This is login page"
    }

@auth_router.post("/login")
async def login(user: LoginModel):
    check_user = session.query(User).filter(User.username == user.username).first()

    if check_user and security.check_password_hash(check_user.password, user.password):
        return HTTPException(status_code=status.HTTP_200_OK, detail="Login successfully")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"username yoki password xato")


@auth_router.get("/register")
async def register():
    return {
        "message": "This is register page"
    }


@auth_router.post("/register")
async def register(user: RegisterModel):
    username = session.query(User).filter(User.username == user.username).first()
    # if username is not None:
    #     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday username ega "
    #                                                                          "foydalanuvchi allaqachon mavjud")

    email = session.query(User).filter(User.email == user.email).first()

    if email or username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday "
                                                                             "foydalanuvchi allaqachon mavjud")

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=security.generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="successfully")


@auth_router.get("/list")
async def users_data(status_code=status.HTTP_200_OK):
    users = session.query(User).all()
    context = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_active": user.is_active
        }
        for user in users
    ]
    return jsonable_encoder(context)