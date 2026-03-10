import pymysql
pymysql.install_as_MySQLdb()
from main import app, db, product

with app.app_context():
    products = product.query.all()
    print(f"Product count: {len(products)}")
    for p in products:
        print(f"ID: {p.sno}, Name: {p.name}")
