from flask import Flask, render_template
from flask_login import login_required, current_user
from config import Config
from models import db
from routes.auth_routes import auth, login_manager
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.market_routes import market_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(product_bp, url_prefix="/products")

app.register_blueprint(order_bp, url_prefix="/orders")
app.register_blueprint(market_bp, url_prefix="/markets")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", current_user=current_user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
