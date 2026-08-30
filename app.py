import os
from flask import Flask, render_template
from database.models import db


# =========================================
# APPLICATION SETUP
# =========================================

app = Flask(__name__)


# =========================================
# SECRET KEY
# =========================================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-secret-key-change-before-deployment"
)


# =========================================
# DATABASE CONFIGURATION
# =========================================

# For development we can use SQLite.
#
# Later, when we deploy the system, we will
# connect this application to PostgreSQL.

database_url = os.environ.get(
    "DATABASE_URL",
    "sqlite:///library_membership.db"
)

# Some hosting platforms provide PostgreSQL
# URLs beginning with postgres://.
# SQLAlchemy expects postgresql://.

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================
# INITIALISE DATABASE
# =========================================

db.init_app(app)


# =========================================
# CREATE DATABASE TABLES
# =========================================

with app.app_context():
    db.create_all()


# =========================================
# PUBLIC PAGES
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


@app.route("/application-success")
def application_success():
    return render_template(
        "application-success.html"
    )


# =========================================
# ADMIN PAGES
# =========================================

@app.route("/admin/login")
def admin_login():
    return render_template(
        "admin-login.html"
    )


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template(
        "admin-dashboard.html"
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
