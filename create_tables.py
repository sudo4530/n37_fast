from database import ENGINE, Base
from models import User, Product, Category, Order
Base.metadata.create_all(ENGINE)


