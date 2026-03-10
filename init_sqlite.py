import main
from main import db, product, User, Review, order_detail

def init_db():
    with main.app.app_context():
        # This will create all tables in the sqlite db
        db.create_all()
        
        # Check if products already exist
        if product.query.count() == 0:
            products = [
                product(sno=1, name='lavender', price=150, detail='for dry skin '),
                product(sno=2, name='beetroot lipbalm', price=70, detail='to cure chaped and dry lips made with natural oils .. also available in alovera ,sandalwood,coffe , limegrass flavors'),
                product(sno=3, name='alovera aqua bass crème', price=120, detail='for oily skin '),
                product(sno=4, name='milkkesar soap', price=150, detail='for luxury bath , made with original saffron'),
                product(sno=5, name='Korean rice soap', price=100, detail='for smooth and shiny Korean glass skin'),
                product(sno=6, name='haldikesar soap', price=150, detail='made with organic haldi and real saffron'),
                product(sno=7, name='organic shampoo', price=100, detail='made with 13 auyrvedic materials '),
                product(sno=8, name='rose soap', price=60, detail=''),
                product(sno=9, name='front page of soap category', price=0, detail=''),
                product(sno=10, name='organic hair oil', price=120, detail='made with 5 ayurvedic materials for shiny and strong hair'),
                product(sno=11, name='body scrub soap', price=70, detail='for exfoliation'),
                product(sno=12, name='charcoal soap', price=70, detail='for tan free skin'),
                product(sno=13, name='ubtan soap', price=80, detail='gives you a spa like skin'),
                product(sno=14, name='resin pen', price=60, detail='perfect for gift and stylish way to write')
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
            print("Database initialized with product data for SQLite!")
        else:
            print("Database already contains product data.")

if __name__ == "__main__":
    init_db()
