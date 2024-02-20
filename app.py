from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qwerty'

app.config['STATIC_FOLDER'] = 'static'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))

                             # Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)




@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        
        # Save the uploaded image to the 'images' folder in the current working directory
        image = request.files['image']
        # image_filename = secure_filename(image.filename)  # Use secure_filename to sanitize the filename
        image_path = os.path.join('images')
        image.save(image_path)
        
        new_product = Product(name=name, price=price, image=image_path)
        
        with app.app_context():
            db.session.add(new_product)
            db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])

        # Check if a new image file is provided
        if 'image' in request.files:
            new_image = request.files['image']
            if new_image:
                # Save the new image to the 'images' folder in the current working directory
                # new_image_filename = secure_filename(new_image.filename)
                new_image_path = os.path.join('images')
                new_image.save(new_image_path)
                product.image = new_image_path

        with app.app_context():
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        # with app.app_context():
        db.session.delete(product)
        db.session.commit()
        flash(f'The product "{product.name}" has been deleted successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('delete_product.html', product=product)



if __name__ == '__main__':
    app.run(debug=True)
