import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Product
from forms import ProductForm
from werkzeug.utils import secure_filename

product_bp = Blueprint('product', __name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@product_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'farmer':
        flash("Only farmers can add products.", "danger")
        return redirect(url_for('dashboard'))

    form = ProductForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(UPLOAD_FOLDER, image_filename))

        product = Product(
            name=form.name.data,
            price=form.price.data,
            quantity=form.quantity.data,
            image=image_filename,
            farmer_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('product.view_products'))

    return render_template('add_product.html', form=form)

@product_bp.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@product_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.farmer_id != current_user.id:
        flash("You are not authorized to edit this product.", "danger")
        return redirect(url_for('dashboard'))

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(UPLOAD_FOLDER, image_filename))
            product.image = image_filename
        
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('product.view_products'))

    return render_template('edit_product.html', form=form, product=product)

@product_bp.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.farmer_id != current_user.id:
        flash("You are not authorized to delete this product.", "danger")
        return redirect(url_for('dashboard'))

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('product.view_products'))
