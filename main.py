from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_mail import Mail, Message
import random
import qrcode
from datetime import datetime
import json
app=Flask(__name__)
app.secret_key = "super_secret_key_for_nova_mart"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orma.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class product(db.Model):
    sno = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price= db.Column(db.Integer(), nullable=False)
    detail= db.Column(db.String(100), nullable=False)
class order_detail(db.Model):
    sno = db.Column(db.Integer(), nullable=False, primary_key=True)
    order_id= db.Column(db.String(100), nullable=False)
    product = db.Column(db.Integer(), nullable=False)
    customer_name= db.Column(db.String(100), nullable=False)
    customer_address= db.Column(db.String(100), nullable=False)
    customer_mobile= db.Column(db.String(100), nullable=False)
    tid= db.Column(db.String(100), nullable=False)
    amt= db.Column(db.Integer(), nullable=False)
    session_id= db.Column(db.String(100), nullable=False)
    session_id= db.Column(db.String(100), nullable=False)
    date= db.Column(db.String(100), nullable=False)

class Review(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True, default='default.jpg')
    joined_at = db.Column(db.DateTime, default=datetime.now)

@app.route("/")
def main():
    return redirect("/index")


@app.route("/index")
def index():    
    products = product.query.order_by(func.random()).limit(4).all()
    return render_template("index.html",pd=products)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
    
@app.route("/login_email", methods=["POST"])
def login_email():
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        session['user'] = email
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create new user
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            return "new_user" # Signal frontend to redirect to complete_profile
        
        # Check if profile is complete (name is present)
        if not user.name:
            return "incomplete"
            
    return "done"

@app.route("/complete_profile", methods=["GET", "POST"])
def complete_profile():
    if 'user' not in session:
        return redirect("/login")
        
    if request.method == "POST":
        try:
            name = request.form.get("name")
            gender = request.form.get("gender")
            
            user = User.query.filter_by(email=session['user']).first()
            if not user:
                return "User not found", 404

            # Handle Profile Pic Upload
            if 'profile_pic' in request.files:
                file = request.files['profile_pic']
                if file.filename != '':
                    import os
                    from werkzeug.utils import secure_filename
                    filename = secure_filename(f"user_{session['user']}_{file.filename}")
                    filepath = os.path.join("static/img/users", filename)
                    os.makedirs("static/img/users", exist_ok=True)
                    file.save(filepath)
                    user.profile_pic = filename
            
            # Update User Details
            user.name = name
            user.gender = gender
            db.session.commit()
            
            return redirect("/")
        except Exception as e:
            print(f"Error in complete_profile: {e}")
            return f"An error occurred: {e}", 500
        
    return render_template("complete_profile.html")
@app.route("/logout")
def logout():
    if ('user' in session):
        session.pop("user")
    return redirect("/")
@app.route("/contact")
def contact():
	return render_template("contact.html")
@app.route("/about")
def about():
	return render_template("about.html")
@app.route("/shop")
def shop():
    query = request.args.get('q')
    if query:
        # Case-insensitive search using ilike
        products = product.query.filter(product.name.ilike(f'%{query}%')).all()
    else:
        products = product.query.all()
    return render_template("shop.html", pd=products, search_query=query)

@app.route("/single_item/<string:sno>")
def single_item(sno):
    products = product.query.filter_by(sno=sno).first()
    reviews = Review.query.filter_by(product_id=sno).order_by(Review.date.desc()).all()
    avg_rating = 0
    if reviews:
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        avg_rating = round(avg_rating, 1)
    return render_template("single_itme.html", pd=products, reviews=reviews, avg_rating=avg_rating)

@app.route("/add_review/<int:sno>", methods=["POST"])
def add_review(sno):
    if 'user' in session:
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        new_review = Review(
            product_id=sno,
            user_email=session['user'],
            rating=int(rating),
            comment=comment,
            date=datetime.now()
        )
        db.session.add(new_review)
        db.session.commit()
    return redirect(f"/single_item/{sno}")
    
@app.route("/billing/<string:sno>")
def billing(sno):
    if ('user' in session):
        products = product.query.filter_by(sno=sno).first()
        return render_template("billing.html",pd=products)
    return redirect("/login")
@app.route("/payment/<string:sno>",methods=["POST"])
def payment(sno):  
    if ('user' in session):
        if request.method == "POST":
            name = request.form["name"]
            address = request.form["address"]
            mobile = request.form["mobile"]
            products = product.query.filter_by(sno=sno).first()
            order_id=random.randint(10**11, 10**12 - 1)
            new_order = order_detail(
            order_id = order_id,
            product = sno,
            customer_name = name,
            customer_address = address,
            customer_mobile = mobile,
            session_id=session["user"],
            tid=0,
            amt=products.price,
            date=datetime.now()
            )
            db.session.add(new_order)
            db.session.commit() 
            return redirect(f"/make_payment/{order_id}")
            return render_template("payment.html",order_id=order_id) 
    return redirect("/")
@app.route("/make_payment/<string:sno>")
def make_payment(sno):  
    if ('user' in session):
        orders = order_detail.query.filter_by(order_id=sno).all()
        if not orders:
             return redirect("/")
        
        total_amt = sum([o.amt for o in orders])
        # Pass the first order object for common details, but overwrite amount
        orders[0].amt = total_amt
        return render_template("payment.html",o_id=orders[0]) 
    return redirect("/")
@app.route("/payment_done/<string:sno>",methods=["POST"])
def payment_done(sno):  
    if ('user' in session):
        if request.method == "POST":
            utr = request.form["utr"]
            orders = order_detail.query.filter_by(order_id=sno).all()
            if orders and utr!="0":
                for o in orders:
                    o.tid = utr
                db.session.commit()
                return redirect("/done") 

@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        # Fetch orders for the current user
        # We need to manually join with product table since there is no relationship defined
        orders = db.session.query(order_detail, product).join(product, order_detail.product == product.sno).filter(order_detail.session_id == session['user']).order_by(order_detail.date.desc()).all()
        return render_template("dashboard.html", orders=orders)
    return redirect("/login")
@app.route("/cart")
def cart():
    cart_cookie = request.cookies.get('cart')
    cart_data = []
    total_amount = 0
    has_items = False
    
    if cart_cookie and cart_cookie.strip():
        # Parse "id1,id2,id1,id3"
        item_ids = [id for id in cart_cookie.split(",") if id.strip()]
        
        if item_ids:
            has_items = True
            # Count frequencies
            from collections import Counter
            counts = Counter(item_ids)
            unique_ids = list(counts.keys())
            
            # Fetch unique products
            products = product.query.filter(product.sno.in_(unique_ids)).all()
            
            # Build detailed list
            for p in products:
                qty = counts[str(p.sno)]
                line_total = p.price * qty
                total_amount += line_total
                cart_data.append({
                    'sno': p.sno,
                    'name': p.name,
                    'price': p.price,
                    'img': f"/static/img/pdimg/{p.sno}/01.jpeg",
                    'qty': qty,
                    'total': line_total
                })
                
    return render_template("cart.html", cart_items=cart_data, total_amount=total_amount, has_items=has_items)

@app.route("/billing_cart")
def billing_cart():
    if 'user' not in session:
        return redirect("/login")
    return render_template("billing.html", action_url="/place_order_cart")

@app.route("/place_order_cart", methods=["POST"])
def place_order_cart():
    if 'user' not in session:
        return redirect("/login")
        
    name = request.form["name"]
    address = request.form["address"]
    mobile = request.form["mobile"]
    
    # Get cart items from cookie
    cart = request.cookies.get('cart')
    if not cart:
        return redirect("/cart")
        
    cart_items = cart.split(",")
    # Get all products to lookup prices
    all_products = product.query.filter(product.sno.in_(cart_items)).all()
    product_map = {str(p.sno): p for p in all_products}
    
    order_id = random.randint(10**11, 10**12 - 1)
    
    for item_id in cart_items:
        if item_id in product_map:
            prod = product_map[item_id]
            new_order = order_detail(
                order_id = str(order_id),
                product = prod.sno,
                customer_name = name,
                customer_address = address,
                customer_mobile = mobile,
                session_id=session["user"],
                tid="0",
                amt=prod.price,
                date=datetime.now()
            )
            db.session.add(new_order)
            
    db.session.commit()
    
    # Clear cart cookie
    resp = redirect(f"/make_payment/{order_id}")
    resp.set_cookie('cart', '', expires=0)
    return resp

@app.route("/done")
def done():
    return render_template("done.html")
@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if not q:
        return json.dumps([])
    
    # Simple case-insensitive search
    # Using format() to inject % wildcards safely with SQLAlchemy
    results = product.query.filter(product.name.ilike(f"%{q}%")).limit(5).all()
    
    data = []
    for p in results:
        # Correct image path to match shop.html logic
        img_path = f"/static/img/pdimg/{p.sno}/01.jpeg" 
        
        data.append({
            "id": p.sno,
            "name": p.name,
            "price": p.price,
            "image": img_path
        })
        
    return json.dumps(data)

# --- MASTER DASHBOARD (ADMIN) ---
@app.route("/master")
def master():
    # TODO: Add proper admin verification here
    if 'user' in session:
        return render_template("master_dashboard.html")
    return redirect("/login")

@app.route("/master/add_product", methods=["POST"])
def add_product():
    if 'user' not in session:
        return redirect("/login")
        
    try:
        name = request.form.get("name")
        price = request.form.get("price")
        detail = request.form.get("detail")
        
        # 1. Create Product Record
        new_prod = product(
            name=name,
            price=int(price),
            detail=detail
        )
        db.session.add(new_prod)
        db.session.commit() # Commit to generate sno
        
        # 2. Handle Image Upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                import os
                # Create directory: static/img/pdimg/{sno}
                save_dir = os.path.join("static", "img", "pdimg", str(new_prod.sno))
                os.makedirs(save_dir, exist_ok=True)
                
                # Save as 01.jpeg (standard convention for this app)
                file.save(os.path.join(save_dir, "01.jpeg"))
                
        return redirect("/shop")
        
    except Exception as e:
        print(f"Error adding product: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)