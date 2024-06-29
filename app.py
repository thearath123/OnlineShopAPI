from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

# Fake API endpoint for multiple products
FAKE_API_URL = 'https://fakestoreapi.com/products'
TELEGRAM_BOT_TOKEN = '6921614796:AAF9rZGEIGLM2gSAhJfPwZFHkbFjHasCjoQ'
TELEGRAM_CHAT_ID = '@Thearathss25'  # Use '@your_channel_username' for public channels or '-1001234567890' for private channels


@app.route('/')
@app.route('/dashboard')
def dashboard():
    try:
        response = requests.get(FAKE_API_URL)
        response.raise_for_status()
        products = response.json()
        print(f"Fetched products: {products}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        products = []

    module = 'dashboard'
    return render_template('dashboard.html', module=module, products=products)



@app.route('/shopItem')
def shop_item():
    product_id = request.args.get('id')
    print(f"Fetching product with ID: {product_id}")

    try:
        response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
        response.raise_for_status()
        product = response.json()
        print(f"Fetched product: {product}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        product = {}

    module = 'shop_item'
    return render_template('shop-item.html', module=module, product=product)


@app.route('/checkout')
def checkout():
    product_id = request.args.get('id')
    print(f"Fetching product for checkout with ID: {product_id}")

    try:
        response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
        response.raise_for_status()
        product = response.json()
        print(f"Fetched product for checkout: {product}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        product = {}

    module = 'checkout'
    return render_template('checkout-item.html', module=module, product=product)


@app.route('/handle_checkout', methods=['POST'])
def handle_checkout():
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    zip_code = request.form.get('zip')
    product_id = request.form.get('product_id')

    try:
        response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
        response.raise_for_status()
        product = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return redirect(url_for('checkout', id=product_id))

    message = (
        f"New Checkout:\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Address: {address}, {city}, {zip_code}\n"
        f"Product: {product['title']}\n"
        f"Price: ${product['price']}\n"
    )

    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        requests.post(telegram_url, data=payload)
        print(f"Sent message to Telegram: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

    return redirect(url_for('checkout', id=product_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
