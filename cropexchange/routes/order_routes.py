from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Order, Product
from forms import OrderForm

order_bp = Blueprint('order', __name__)

@order_bp.route('/place_order/<int:product_id>', methods=['GET', 'POST'])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)

    if current_user.role != 'buyer':
        flash("Only buyers can place orders.", "danger")
        return redirect(url_for('dashboard'))

    form = OrderForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity > product.quantity:
            flash("Not enough stock available!", "danger")
            return redirect(url_for('order.place_order', product_id=product.id))

        total_price = quantity * product.price
        order = Order(product_id=product.id, buyer_id=current_user.id, quantity=quantity, total_price=total_price)
        product.quantity -= quantity  # Reduce stock

        db.session.add(order)
        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for('order.view_orders'))

    return render_template('place_order.html', form=form, product=product)

@order_bp.route('/orders')
@login_required
def view_orders():
    if current_user.role == 'buyer':
        orders = Order.query.filter_by(buyer_id=current_user.id).all()
    elif current_user.role == 'farmer':
        orders = Order.query.join(Product).filter(Product.farmer_id == current_user.id).all()
    else:
        orders = []

    return render_template('view_orders.html', orders=orders)

@order_bp.route('/update_order/<int:order_id>/<string:status>', methods=['POST'])
@login_required
def update_order(order_id, status):
    order = Order.query.get_or_404(order_id)

    if order.product.farmer_id != current_user.id:
        flash("You are not authorized to update this order.", "danger")
        return redirect(url_for('dashboard'))
     # Reduce stock
    # order.product.quantity -= order.quantity

    if status in ["Approved", "Shipped", "Delivered", "Rejected"]:
        order.status = status
        db.session.commit()
        flash(f"Order {status} successfully!", "success")
    else:
        flash("Invalid status update.", "danger")

    return redirect(url_for('order.view_orders'))
