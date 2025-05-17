# from app import app
# from models.db import db
# from models.payment_method import PaymentMethod

# methods = [
#     {
#         "type": "Lightning",
#         "provider_name": "LND",
#         "description": "Lightning Network Daemon"
#     },
#     {
#         "type": "MobileMoney",
#         "provider_name": "MTN Momo",
#         "description": "Mobile money service in Africa"
#     },
#     {
#         "type": "MobileMoney",
#         "provider_name": "Airtel Money",
#         "description": "Airtel mobile money service"
#     },
#     {
#         "type": "MobileMoney",
#         "provider_name": "M-Pesa",
#         "description": "Dummy M-Pesa entry for testing"
#     },
# ]

# with app.app_context():
#     for m in methods:
#         exists = PaymentMethod.query.filter_by(
#             type=m["type"],
#             provider_name=m["provider_name"]
#         ).first()
#         if not exists:
#             db.session.add(PaymentMethod(**m))
#             print(f"Seeded: {m['provider_name']}")
#         else:
#             print(f"Skipped (exists): {m['provider_name']}")
#     db.session.commit()
#     print("Seeding complete.")

from app import app
from models.db import db
from models.payment_method import PaymentMethod
from models.mobile_money_prov import MobileMoneyProv  # Adjust path if needed

payment_methods = [
    {
        "type": "Lightning",
        "provider_name": "LND",
        "description": "Lightning Network Daemon"
    },
    {
        "type": "MobileMoney",
        "provider_name": "MTN Momo",
        "description": "Mobile money service in Africa"
    },
    {
        "type": "MobileMoney",
        "provider_name": "Airtel Money",
        "description": "Airtel mobile money service"
    },
    {
        "type": "MobileMoney",
        "provider_name": "M-Pesa",
        "description": "Dummy M-Pesa entry for testing"
    },
]

mobile_providers = [
    {
        "provider_name": "MTN Momo",
        "api_url": "http://localhost:5001/api/mtn/payment",
        "country": "UG"
    },
    {
        "provider_name": "Airtel Money",
        "api_url": "http://localhost:5001/api/airtel/payment",
        "country": "UG"
    },
    {
        "provider_name": "M-Pesa",
        "api_url": "http://localhost:5001/api/mpesa/payment",
        "country": "KE"
    },
]

with app.app_context():
    # Seed payment methods
    for m in payment_methods:
        exists = PaymentMethod.query.filter_by(
            type=m["type"],
            provider_name=m["provider_name"]
        ).first()
        if not exists:
            db.session.add(PaymentMethod(**m))
            print(f"Seeded PaymentMethod: {m['provider_name']}")
        else:
            print(f"Skipped (exists): {m['provider_name']}")

    # Seed mobile money providers
    for p in mobile_providers:
        exists = MobileMoneyProv.query.filter_by(provider_name=p["provider_name"]).first()
        if not exists:
            db.session.add(MobileMoneyProv(**p))
            print(f"Seeded MobileMoneyProv: {p['provider_name']}")
        else:
            print(f"Skipped (exists): {p['provider_name']}")

    db.session.commit()
    print("Seeding complete.")
