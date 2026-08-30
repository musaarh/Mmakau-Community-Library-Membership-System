from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class MembershipApplication(db.Model):
    """
    Stores library membership applications.
    """

    __tablename__ = "membership_applications"

    id = db.Column(db.Integer, primary_key=True)

    # =========================================
    # APPLICANT INFORMATION
    # =========================================

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    id_number = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    # =========================================
    # CONTACT INFORMATION
    # =========================================

    email = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    # =========================================
    # ADDRESS
    # =========================================

    address = db.Column(
        db.Text,
        nullable=False
    )

    # =========================================
    # MEMBERSHIP
    # =========================================

    membership_type = db.Column(
        db.String(50),
        nullable=False
    )

    # =========================================
    # APPLICATION STATUS
    # =========================================

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    # =========================================
    # LIBRARY BARCODE
    # =========================================

    # The librarian enters an existing barcode
    # after the application has been approved.
    barcode = db.Column(
        db.String(100),
        nullable=True,
        unique=True
    )

    # =========================================
    # ADMIN NOTES
    # =========================================

    admin_notes = db.Column(
        db.Text,
        nullable=True
    )

    # =========================================
    # DATES
    # =========================================

    application_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    reviewed_date = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================================
    # REPRESENTATION
    # =========================================

    def __repr__(self):
        return (
            f"<MembershipApplication "
            f"{self.first_name} {self.last_name} "
            f"- {self.status}>"
        )
