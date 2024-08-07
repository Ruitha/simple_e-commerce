import requests #type: ignore
import logging, os, sys

from venv import create
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from model import db, Product, Order #type: ignore
from intasend import APIService # type: ignore
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db= SQLAlchemy(app)
db.init_app(app)


# Creating tables in the Database(Database initialization)
def create_db():
    with app.app_context():
        if not os.path.exists('ecommerce.db'):
            db.create_all()


@app.route('/')
def index():

    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Print form data for debugging
        # print(request.form)
        print(request.form)
        

        token = os.getenv('IS_SECRET_KEY')
        publishable_key = os.getenv('IS_PUBLISHABLE_KEY')
        service = APIService(token=token, publishable_key=publishable_key, test=True)

        payment_details = {
            'phone_number': request.form['customer_phone'],
            'first_name': request.form['customer_name'].split(" ")[0],
            'last_name': request.form['customer_name'].split(" ")[-1],
            # 'description': request.form['description']
        }

        try:
            response = service.collect.checkout(amount= float(request.form['amount'], redirect_url=""),#add a redirect url of your choice
            currency= request.form['currency'],
            email=request.form['customer_email'],**payment_details)
            logger.debug(f"Payment response: {response}")
            try:
                return redirect(response.get("url"))
            except:
                flash('Payment failed: {}'.format(response))
                return render_template('checkout.html')
        except Exception as e:
            logger.exception("Error processing payment")
            flash('Error processing payment: {}'.format(str(e)))
            return render_template('checkout.html')
    return render_template('checkout.html')

@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)
    create_db()
    app.debug = True
    app.run()

