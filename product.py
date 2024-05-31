from fastapi import APIRouter, status, HTTPException
from models import Product, Category
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE
from schemas import ProductModel

session = session(bind=ENGINE)

product_router =