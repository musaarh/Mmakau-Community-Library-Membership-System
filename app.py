from flask import Flask, render_template


# =========================================
# APPLICATION SETUP
# =========================================

app = Flask(__name__)

# Secret key
# -----------------------------------------
# For development, this fallback value is
# acceptable.
#
# Before deployment, we will put the real
# secret key in an environment variable.
# -----------------------------------------

import os

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-secret-key-change-before-deployment"
)


# =========================================
# PUBLIC PAGES
# =========================================

@app.route("/")
def home():
    """
    Membership system home page.
    """
    return render_template("index.html")


@app.route("/apply")
def apply():
    """
    Membership application page.
    """
    return render_template("apply.html")


@app.route("/application-success")
def application_success():
    """
    Page shown after an application has
    successfully been submitted.
    """
    return render_template("application-success.html")


# =========================================
# ADMIN PAGES
# =========================================

@app.route("/admin/login")
def admin_login():
    """
    Librarian/admin login page.
    """
    return render_template("admin-login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    """
    Librarian/admin dashboard.

    Authentication will be added before
    this page is used in production.
    """
    return render_template("admin-dashboard.html")


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
