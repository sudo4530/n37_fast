from models import Order, User, Product
from schemas import OrderModel, UserOrder
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE

session = session(bind=ENGINE)
order_router = APIRouter(prefix="/orders")

@order_router.get('/')
async def orders():
    orders = session.query(Order).all()
    context = [
        {
            "id": order.id,
            "user": {
                "id": order.users.id,
                "first_name": order.users.first_name,
                "last_name": order.users.last_name,
                "username": order.users.username,
                "email": order.users.email,
                "is_staff": order.users.is_staff,
                "is_active": order.users.is_active
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "category": {
                    "id": order.product.category.id,
                    "name": order.product.category.name
                }
            },
            "status": order.order_status
        }
        for order in orders
    ]
    return jsonable_encoder(context)

@order_router.post('/create')
async def create(order: OrderModel):
    check_order = session.query(Order).filter(Order.id == order.id).first()
    check_user_id = session.query(User).filter(User.id == order.user_id).first()
    check_product_id = session.query(Product).filter(Product.id == order.product_id).first()

    if check_order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exist")

    elif check_user_id and check_product_id:
        new_order = Order(
            id=order.id,
            product_id=order.product_id,
            user_id=order.user_id,
            count=order.count,
            order_status=order.order_status
        )
        session.add(new_order)
        session.commit()
        data = {
            "success": True,
            "code": 201,
            "msg": "created success",
            "data": {
                "id": new_order.id,
                "user": {
                    "id": new_order.users.id,
                    "first_name": new_order.users.first_name,
                    "last_name": new_order.users.last_name,
                    "username": new_order.users.username,
                    "email": new_order.users.email,
                    "is_staff": new_order.users.is_staff,
                    "is_active": new_order.users.is_active
                },
                "product": {
                    "id": new_order.product.id,
                    "name": new_order.product.name,
                    "price": new_order.product.price,
                    "category": {
                        "id": new_order.product.category.id,
                        "name": new_order.product.category.name
                    }
                },
                "count": new_order.count,
                "status": new_order.order_status
            }
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id or product_id already exist")


@order_router.get("/{id}")
async def get_order_id(id: int):
    check_order = session.query(Order).filter(Order.id == id).first()
    if check_order:
        data = {
            "success": True,
            "code": 201,
            "msg": "created success",
            "data": {
                "id": check_order.id,
                "user": {
                    "id": check_order.users.id,
                    "first_name": check_order.users.first_name,
                    "last_name": check_order.users.last_name,
                    "username": check_order.users.username,
                    "email": check_order.users.email,
                    "is_staff": check_order.users.is_staff,
                    "is_active": check_order.users.is_active
                },
                "product": {
                    "id": check_order.product.id,
                    "name": check_order.product.name,
                    "price": check_order.product.price,
                    "category": {
                        "id": check_order.product.category.id,
                        "name": check_order.product.category.name
                    }
                },
                "count": check_order.count,
                "status": check_order.order_status,
                "total_balance": check_order.product.price * check_order.count,
                "total_balance_promo_cod": check_order.product.price * check_order.count
            }
        }
        promo_code = "uz"
        if promo_code == "uzum":
            data['data']["total_balance_promo_cod"] *= 0.9
            return jsonable_encoder(data)
        else:
            return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bunday order mavjud emas")



@order_router.post("/user/order")
async def get_user_orders(user_order: UserOrder):
    check_user = session.query(User).filter(User.username == user_order.username).first()
    if check_user and check_user.is_staff:
        print("ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        check_order = session.query(Order).filter(Order.user_id == check_user.id)
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {check_order.count}")
        if check_order:
            print("ERROR ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            context = [
                {
                    "id": order.id,
                    "user": {
                        "id": order.users.id,
                        "first_name": order.users.first_name,
                        "last_name": order.users.last_name,
                        "username": order.users.username,
                        "email": order.users.email,
                        "is_staff": order.users.is_staff,
                        "is_active": order.users.is_active
                    },
                    "product": {
                        "id": order.product.id,
                        "name": order.product.name,
                        "price": order.product.price,
                        "category": {
                            "id": order.product.category.id,
                            "name": order.product.category.name
                        }
                    },
                    "status": order.order_status,
                    "total_price": order.count * order.product.price
                }
                for order in check_order
            ]
            return jsonable_encoder(context)
        else:
            return HTTPException(status_code=status.HTTP_200_OK, detail="Bu foydalanuvchini buyurtmalari mavjud emas")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu foydalanuvchi mavjud emas")


@order_router.post("/user/order/price")
async def get_user_orders(user_order: UserOrder):
    check_user = session.query(User).filter(User.username == user_order.username).first()
    if check_user:
        print("ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        check_order = session.query(Order).filter(Order.user_id == check_user.id)
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {check_order.count}")
        if check_order:
            total_balance = 0
            product_count = 0
            for order in check_order:
                total_balance += order.count * order.product.price
                product_count += 1
            data = {
                "status": 200,
                "msg": "total balance",
                "data": {
                    "product_count": product_count,
                    "total_price": total_balance
                }
            }
            return jsonable_encoder(data)