import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.security import check_password_hash
from database.models import db, MembershipApplication


# =========================================
# APPLICATION SETUP
# =========================================

app = Flask(__name__)

@app.context_processor
def inject_current_year():
    return {
        "current_year": datetime.now().year
    }


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

database_url = os.environ.get(
    "DATABASE_URL",
    "sqlite:///library_membership.db"
)

# Some hosting platforms use postgres://
# while SQLAlchemy expects postgresql://

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
# HOME
# =========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================
# MEMBERSHIP APPLICATION
# =========================================

@app.route("/apply", methods=["GET", "POST"])
def apply():

    # -----------------------------------------
    # SHOW APPLICATION FORM
    # -----------------------------------------

    if request.method == "GET":

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # GET FORM DATA
    # -----------------------------------------

    first_name = request.form.get(
        "first_name",
        ""
    ).strip()

    last_name = request.form.get(
        "last_name",
        ""
    ).strip()

    date_of_birth = request.form.get(
        "date_of_birth",
        ""
    ).strip()

    id_number = request.form.get(
        "id_number",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    membership_type = request.form.get(
        "membership_type",
        ""
    ).strip()


    # -----------------------------------------
    # BASIC VALIDATION
    # -----------------------------------------

    if not all([
        first_name,
        last_name,
        date_of_birth,
        id_number,
        email,
        phone,
        address,
        membership_type
    ]):

        flash(
            "Please complete all required fields.",
            "error"
        )

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # VALIDATE DATE
    # -----------------------------------------

    try:

        birth_date = datetime.strptime(
            date_of_birth,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        flash(
            "Please enter a valid date of birth.",
            "error"
        )

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # CHECK MEMBERSHIP TYPE
    # -----------------------------------------

    allowed_membership_types = [
        "Children",
        "Adults",
        "Pensioners"
    ]

    if membership_type not in allowed_membership_types:

        flash(
            "Please select a valid membership type.",
            "error"
        )

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # CHECK WHETHER ID ALREADY EXISTS
    # -----------------------------------------

    existing_application = (
        MembershipApplication.query
        .filter_by(id_number=id_number)
        .first()
    )

    if existing_application:

        flash(
            "An application with this ID number "
            "already exists.",
            "error"
        )

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # CREATE APPLICATION
    # -----------------------------------------

    application = MembershipApplication(

        first_name=first_name,

        last_name=last_name,

        date_of_birth=birth_date,

        id_number=id_number,

        email=email,

        phone=phone,

        address=address,

        membership_type=membership_type,

        status="Pending"
    )


    # -----------------------------------------
    # SAVE APPLICATION
    # -----------------------------------------

    try:

        db.session.add(application)

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Something went wrong while submitting "
            "your application. Please try again.",
            "error"
        )

        return render_template(
            "apply.html"
        )


    # -----------------------------------------
    # APPLICATION SUCCESS
    # -----------------------------------------

    return redirect(
        url_for(
            "application_success"
        )
    )


# =========================================
# APPLICATION SUCCESS
# =========================================

@app.route("/application-success")
def application_success():

    return render_template(
        "application-success.html"
    )


# =========================================
# ADMIN LOGIN
# =========================================

@app.route("/admin/login")
def admin_login():

    return render_template(
        "admin-login.html"
    )


# =========================================
# ADMIN DASHBOARD
# =========================================

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
