from fastapi import APIRouter, status, HTTPException
from models import Product, Category
from schemas import ProductModel, CategoryModel
from database import session, ENGINE
from fastapi.encoders import jsonable_encoder

product_router = APIRouter(prefix='/product')
session = session(bind=ENGINE)

@product_router.get('/')
async def product_list():
    products = session.query(Product).all()
    category = session.query(Category).filter()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id
        }
        for product in products
    ]
    return jsonable_encoder(context)

@product_router.post('/create')
async def product_create(product: ProductModel):
    check_product_id = session.query(Product).filter(Product.id == product.id).first()
    check_category_id = session.query(Category).filter(Category.id == product.category_id).first()
    if (check_product_id and check_category_id) or (check_product_id and check_category_id is None):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu product allaqachon mavjud")

    # elif check_product_id is None and check_category_id:
    new_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )
    session.add(new_product)
    session.commit()
    data = {
        "code": 201,
        "success": True,
        "msg": "Created new product",
        "data": {
            "id": new_product.id,
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "category": {
                "id": new_product.category.id,
                "name": new_product.category.name
            }
        }
    }
    return data

@product_router.get('/{id}')
async def product_id(id: int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        context = {
            "id": check_product.id,
            "name": check_product.name,
            "description": check_product.description,
            "price": check_product.price,
            "category_id": check_product.category_id,
            }
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday product mavjud emas")


@product_router.put('/{id}')
async def update_product(id: int, data: ProductModel):
    product = session.query(Product).filter(Product.id == id).first()
    check_category_id = session.query(Category).filter(Category.id == data.category_id).first()
    if product:
        if check_category_id:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                "code": 200,
                "message": "Update product"
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed section")

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed section")


@product_router.delete('/{id}')
async def product_delete(id: int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        session.delete(check_product)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not fount")