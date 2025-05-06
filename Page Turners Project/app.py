from flask import Flask, request, redirect, render_template, flash, url_for, make_response, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import bcrypt
import datetime
import random
import string
import threading
from time import sleep
from decimal import Decimal
import logging
import time
import traceback
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
# app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here' 
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()


# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="page_turners",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/test_connection")
def test_connection():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")  # Simple query to test connection
            return "Connection Successful"
    except Exception as e:
        return f"Error: {e}"



def get_user_id_from_cookie():
    return request.cookies.get("user_id")

def set_secure_cookie(response, user_id):
    response.set_cookie("user_id", str(user_id), max_age=3600, httponly=True, secure=True, samesite='Strict')
    return response
def get_db_connection():
    return db

def generate_unique_trx_id(cursor):
    while True:
        trx_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        cursor.execute("SELECT trx_id FROM send_money WHERE trx_id = %s", (trx_id,))
        if not cursor.fetchone():
            return trx_id
@app.route("/test")
def test():
    return render_template("signup.html")

#user_login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode("utf-8"), user['password'].encode("utf-8")):
        resp = make_response(redirect("/home"))
        resp = set_secure_cookie(resp, user["user_id"])
        return resp
    else:
        return render_template("login.html", error="Invalid Email or password.")
    

# SIGN UP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    user_name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            # ✅ Check if user_name or email already exists
            cursor.execute("SELECT * FROM user WHERE email = %s OR user_name = %s", (email, user_name))
            existing = cursor.fetchone()

            if existing:
                if existing['email'] == email:
                    flash("Email already exists. Try a different one.", "error")
                elif existing['user_name'] == user_name:
                    flash("Username already taken. Try another.", "error")
                return render_template("signup.html")

            # ✅ Insert new user
            cursor.execute("""
                INSERT INTO user (user_name, email, password) 
                VALUES (%s, %s, %s)
            """, (user_name, email, hashed_password))
            db.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    except Exception as e:
        print("Signup error:", e)
        flash("Something went wrong. Please try again.", "error")
        return render_template("signup.html")



# Homepage
@app.route('/')
def home():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM book ORDER BY rating DESC LIMIT 10")
            books = cursor.fetchall()
        return render_template('home.html', books=books)
    except Exception as e:
        print("Error fetching books:", e)
        return render_template('home.html', books=[])



# Route to show all authors
@app.route("/authors", methods=["GET"])
def author():
    search_query = request.args.get('search', '')  # Get search query from the URL
    with db.cursor() as cursor:
        if search_query:
            cursor.execute("SELECT author_name, author_img, author_id FROM author WHERE author_name LIKE %s", ('%' + search_query + '%',))
        else:
            cursor.execute("SELECT author_name, author_img, author_id FROM author")
        authors = cursor.fetchall()

    return render_template("author.html", authors=authors)




@app.route('/author_books/<author_id>')
def author_books(author_id):
    # Your code to display books for the given author
    return render_template('author_books.html', author_id=author_id)




# Route to show details of a single author
@app.route("/author/<int:author_id>")
def author_detail(author_id):
    conn = db
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.author_name, a.publications, a.author_img,
            b.date_of_birth, b.award, b.famous_work, b.description
            FROM author a
            JOIN biography b ON a.author_id = b.author_id
            WHERE a.author_id = %s
        """, (author_id,))
        author = cursor.fetchone()
    conn.close()
    return render_template("author_details.html", author=author)

# @app.route('/author')
# def author():
#     return "Author page coming soon!"

@app.route('/user_dashboard')
def user_dashboard():
    return "user_dashboard page coming soon!"

@app.route('/book/<isbn>')
def book_info(isbn):
    # Fetch book by ISBN
    return f"Book details for ISBN: {isbn}"



# ADMIN  
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
                admin = cursor.fetchone()

                if admin:
                    session['admin_logged_in'] = True
                    session['admin_name'] = admin['admin_name']
                    return redirect(url_for('admin_panel'))
                else:
                    flash('Invalid email or password.', 'danger')
        except Exception as e:
            print(f"[ERROR] Admin login failed: {e}")
            traceback.print_exc()  # ← shows the full traceback
            flash('Something went wrong.', 'danger')            
        # except Exception as e:
        #     print(f"[ERROR] Admin login failed: {e}")  # ✅ see actual error in terminal
        #     flash('Something went wrong.', 'danger')

    return render_template('admin_login.html')


# admin panel
@app.route('/admin/panel')
def admin_panel():
    books = []
    reviews = []
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print("Connected to DB:", db_name)

            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("Tables in DB:", tables)

            cursor.execute("SELECT ISBN, book_name, stock FROM book;")
            books = cursor.fetchall()
            print("Books fetched:", books)

            cursor.execute("SELECT * FROM reviews;")
            reviews = cursor.fetchall()
    except Exception as e:
        print("Error:", e)

    return render_template("admin_panel.html", books=books, reviews=reviews)


# ADD BOOKS
@app.route('/admin/add_book', methods=['POST'])
def admin_add_book():
    isbn = request.form['isbn']
    name = request.form['name']
    desc = request.form['desc']
    cover_url = request.form['cover_url']
    language = request.form['language']
    rating = request.form.get('rating') or 0
    stock = request.form.get('stock') or 0
    price = request.form.get('price') or 0.0
    tags = request.form.get('tags') or None
    publication_date = '1900-01-01'  # Or add it to the form later

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM book WHERE ISBN = %s", (isbn,))
            if cursor.fetchone():
                flash('Book with this ISBN already exists.')
                return redirect(url_for('admin_panel'))

            cursor.execute("""
                INSERT INTO book (ISBN, book_name, cover_url, language, publication_date, rating, stock, price, tags, summary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (isbn, name, cover_url, language, publication_date, float(rating), int(stock), float(price), tags, desc))
            db.commit()
            flash('✅ Book added successfully!')
    except Exception as e:
        db.rollback()
        print("Error inserting book:", e)
        flash('❌ Failed to add book.')

    return redirect(url_for('admin_panel'))

# RESTOCK BOOKS
from flask import request, redirect, flash, session

@app.route('/admin/restock', methods=['POST'])
def restock_book():
    isbn = request.form['isbn']
    try:
        qty_change = int(request.form['quantity'])
        with db.cursor() as cursor:
            cursor.execute("UPDATE book SET stock = stock + %s WHERE ISBN = %s", (qty_change, isbn))
            db.commit()
        flash("Stock updated successfully", "success")
    except Exception as e:
        print("Restock error:", e)
        flash("Error updating stock", "error")

    # ✅ Redirect back to admin panel restock section
    return redirect("/admin/panel#restock")


# delete review
@app.route("/admin/delete_review/<int:review_id>")
def delete_review(review_id):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM review WHERE review_id = %s", (review_id,))
    db.commit()
    return redirect("/admin_panel")


# Admin Logout
@app.route('/admin_logout')
def admin_logout():
    session.clear()  # Clear session to log out user
    return redirect(url_for('home'))  # Redirect to home page



# ORDER MANAGEMENT
@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    user_id = session.get("user_id")
    cart = get_cart_items_for_user(user_id)  # however you store cart data

    try:
        with db.cursor() as cursor:
            for item in cart:
                isbn = item['ISBN']
                qty = item['quantity']
                cursor.execute("UPDATE book SET stock = stock - %s WHERE ISBN = %s", (qty, isbn))

            db.commit()
            flash("Order placed successfully!", "success")
    except Exception as e:
        print("Order Error:", e)
        db.rollback()
        flash("Something went wrong with your order.", "error")

    return redirect('/orders')





    
if __name__ == "__main__":
    app.run(debug=True, port=5000)    