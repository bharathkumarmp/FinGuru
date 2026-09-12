import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

NUM_CUSTOMERS = 100
TRANSACTIONS_PER_CUSTOMER = 60


FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rahul",
    "Rohan", "Vikram", "Karan", "Akash", "Nikhil",
    "Ananya", "Priya", "Isha", "Kavya", "Sneha",
    "Meera", "Pooja", "Riya", "Neha", "Diya",
]

LAST_NAMES = [
    "Sharma", "Patel", "Mehta", "Shah", "Verma",
    "Gupta", "Joshi", "Desai", "Singh", "Kumar",
]

CITIES = [
    "Ahmedabad",
    "Gandhinagar",
    "Mumbai",
    "Pune",
    "Bengaluru",
    "Delhi",
    "Jaipur",
    "Surat",
    "Vadodara",
    "Hyderabad",
]

OCCUPATIONS = [
    "Software Engineer",
    "Teacher",
    "Business Owner",
    "Doctor",
    "Accountant",
    "Designer",
    "Marketing Manager",
    "Government Employee",
    "Consultant",
    "Student",
]

MERCHANTS = [
    ("Amazon", "Shopping"),
    ("Flipkart", "Shopping"),
    ("Swiggy", "Food"),
    ("Zomato", "Food"),
    ("Uber", "Transport"),
    ("Ola", "Transport"),
    ("BigBasket", "Groceries"),
    ("Reliance Fresh", "Groceries"),
    ("Netflix", "Entertainment"),
    ("BookMyShow", "Entertainment"),
    ("Apollo Pharmacy", "Healthcare"),
    ("Electricity Board", "Utilities"),
    ("Airtel", "Utilities"),
    ("Jio", "Utilities"),
]

LOAN_TYPES = [
    "Personal Loan",
    "Home Loan",
    "Education Loan",
    "Vehicle Loan",
]

TRANSACTION_TYPES = [
    "DEBIT",
    "DEBIT",
    "DEBIT",
    "CREDIT",
]


# ============================================================
# CUSTOMERS
# ============================================================

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    name = f"{first} {last}"

    email = (
        f"{first.lower()}.{last.lower()}"
        f"{customer_id}@finguru.demo"
    )

    monthly_income = round(
        random.uniform(25000, 180000),
        2,
    )

    customers.append(
        {
            "id": customer_id,
            "customer_code": f"FG{customer_id:05d}",
            "full_name": name,
            "email": email,
            "phone": f"9{random.randint(100000000, 999999999)}",
            "date_of_birth": (
                datetime(
                    random.randint(1970, 2002),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ).date()
            ),
            "city": random.choice(CITIES),
            "occupation": random.choice(OCCUPATIONS),
            "monthly_income": monthly_income,
        }
    )


pd.DataFrame(customers).to_csv(
    DATA_DIR / "customers.csv",
    index=False,
)


# ============================================================
# ACCOUNTS
# ============================================================

accounts = []

for customer in customers:

    customer_id = customer["id"]

    balance = round(
        customer["monthly_income"]
        * random.uniform(0.8, 4.0),
        2,
    )

    accounts.append(
        {
            "id": customer_id,
            "customer_id": customer_id,
            "account_number": f"FGSB{customer_id:010d}",
            "account_type": "savings",
            "balance": balance,
            "currency": "INR",
            "status": "active",
        }
    )


pd.DataFrame(accounts).to_csv(
    DATA_DIR / "accounts.csv",
    index=False,
)


# ============================================================
# TRANSACTIONS
# ============================================================

transactions = []

transaction_id = 1

today = datetime.utcnow()

for customer in customers:

    customer_id = customer["id"]
    income = customer["monthly_income"]

    account_id = customer_id

    # Salary transaction
    transactions.append(
        {
            "id": transaction_id,
            "customer_id": customer_id,
            "account_id": account_id,
            "transaction_type": "CREDIT",
            "amount": income,
            "merchant": "Employer",
            "category": "Salary",
            "location": customer["city"],
            "device_id": f"DEVICE_{customer_id:04d}",
            "beneficiary": None,
            "description": "Monthly salary credit",
            "timestamp": (
                today
                - timedelta(days=random.randint(0, 25))
            ).isoformat(),
        }
    )

    transaction_id += 1

    for _ in range(TRANSACTIONS_PER_CUSTOMER):

        merchant, category = random.choice(MERCHANTS)

        amount = round(
            random.uniform(200, income * 0.08),
            2,
        )

        transactions.append(
            {
                "id": transaction_id,
                "customer_id": customer_id,
                "account_id": account_id,
                "transaction_type": "DEBIT",
                "amount": amount,
                "merchant": merchant,
                "category": category,
                "location": customer["city"],
                "device_id": f"DEVICE_{customer_id:04d}",
                "beneficiary": None,
                "description": f"{category} transaction",
                "timestamp": (
                    today
                    - timedelta(
                        days=random.randint(0, 180)
                    )
                ).isoformat(),
            }
        )

        transaction_id += 1


pd.DataFrame(transactions).to_csv(
    DATA_DIR / "transactions.csv",
    index=False,
)


# ============================================================
# LOANS
# ============================================================

loans = []
loan_id = 1

for customer in customers:

    if random.random() < 0.45:

        principal = round(
            random.uniform(50000, 800000),
            2,
        )

        interest_rate = round(
            random.uniform(8.5, 15.5),
            2,
        )

        tenure = random.choice(
            [12, 24, 36, 48, 60]
        )

        monthly_rate = interest_rate / 12 / 100

        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** tenure
            / (
                (1 + monthly_rate) ** tenure - 1
            )
        )

        outstanding = round(
            principal * random.uniform(0.35, 1.0),
            2,
        )

        loans.append(
            {
                "id": loan_id,
                "customer_id": customer["id"],
                "loan_type": random.choice(LOAN_TYPES),
                "principal_amount": principal,
                "interest_rate": interest_rate,
                "tenure_months": tenure,
                "monthly_emi": round(emi, 2),
                "outstanding_amount": outstanding,
                "status": "active",
            }
        )

        loan_id += 1


pd.DataFrame(loans).to_csv(
    DATA_DIR / "loans.csv",
    index=False,
)


# ============================================================
# EMI RECORDS
# ============================================================

emi_records = []

emi_id = 1

for loan in loans:

    for month in range(1, 7):

        due_date = (
            datetime.utcnow()
            - timedelta(days=30 * (6 - month))
        ).date()

        status = random.choices(
            ["paid", "pending", "missed"],
            weights=[0.82, 0.12, 0.06],
        )[0]

        paid_amount = (
            loan["monthly_emi"]
            if status == "paid"
            else 0
        )

        emi_records.append(
            {
                "id": emi_id,
                "loan_id": loan["id"],
                "customer_id": loan["customer_id"],
                "due_date": due_date.isoformat(),
                "amount": loan["monthly_emi"],
                "paid_amount": paid_amount,
                "status": status,
                "paid_at": (
                    due_date.isoformat()
                    if status == "paid"
                    else None
                ),
            }
        )

        emi_id += 1


pd.DataFrame(emi_records).to_csv(
    DATA_DIR / "emi_records.csv",
    index=False,
)


# ============================================================
# FRAUD EVENTS
# ============================================================

fraud_events = []

fraud_id = 1

for _ in range(30):

    customer = random.choice(customers)

    score = round(
        random.uniform(0.65, 0.99),
        3,
    )

    fraud_events.append(
        {
            "id": fraud_id,
            "customer_id": customer["id"],
            "transaction_id": None,
            "fraud_score": score,
            "risk_level": (
                "HIGH"
                if score >= 0.8
                else "MEDIUM"
            ),
            "status": "open",
            "reason": random.choice(
                [
                    "Unusual transaction amount",
                    "New device detected",
                    "Unusual location",
                    "High transaction frequency",
                    "New beneficiary",
                ]
            ),
            "anomaly_score": round(
                random.uniform(0.6, 1.0),
                3,
            ),
            "rule_score": round(
                random.uniform(0.5, 1.0),
                3,
            ),
            "identity_risk_score": round(
                random.uniform(0.2, 0.9),
                3,
            ),
            "recommended_action": "VERIFY_TRANSACTION",
        }
    )

    fraud_id += 1


pd.DataFrame(fraud_events).to_csv(
    DATA_DIR / "fraud_events.csv",
    index=False,
)


# ============================================================
# PRODUCTS
# ============================================================

products = [
    {
        "product_code": "PL001",
        "name": "Personal Loan",
        "product_type": "loan",
        "description": "Flexible personal loan for eligible customers.",
        "interest_rate": 11.5,
        "min_amount": 50000,
        "max_amount": 1000000,
        "active": True,
    },
    {
        "product_code": "HL001",
        "name": "Home Loan",
        "product_type": "loan",
        "description": "Home financing solution.",
        "interest_rate": 8.5,
        "min_amount": 500000,
        "max_amount": 10000000,
        "active": True,
    },
    {
        "product_code": "FD001",
        "name": "Fixed Deposit",
        "product_type": "investment",
        "description": "Fixed deposit savings product.",
        "interest_rate": 7.0,
        "min_amount": 1000,
        "max_amount": 10000000,
        "active": True,
    },
    {
        "product_code": "RD001",
        "name": "Recurring Deposit",
        "product_type": "investment",
        "description": "Monthly recurring savings product.",
        "interest_rate": 6.5,
        "min_amount": 500,
        "max_amount": 1000000,
        "active": True,
    },
]


with open(
    DATA_DIR / "products.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        products,
        file,
        indent=2,
    )


# ============================================================
# EVENTS
# ============================================================

events = [
    {
        "event_type": "SALARY_CREDITED",
        "description": "Monthly salary credited",
    },
    {
        "event_type": "EMI_DUE",
        "description": "Loan EMI due",
    },
    {
        "event_type": "EMI_MISSED",
        "description": "Loan EMI missed",
    },
    {
        "event_type": "LARGE_TRANSACTION",
        "description": "Large transaction detected",
    },
    {
        "event_type": "NEW_DEVICE",
        "description": "New device detected",
    },
    {
        "event_type": "NEW_BENEFICIARY",
        "description": "New beneficiary added",
    },
    {
        "event_type": "SPENDING_SPIKE",
        "description": "Spending spike detected",
    },
    {
        "event_type": "BALANCE_DROP",
        "description": "Significant balance drop detected",
    },
]


with open(
    DATA_DIR / "events.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        events,
        file,
        indent=2,
    )


# ============================================================
# SUMMARY
# ============================================================

print("\nFinGuru synthetic banking dataset generated.")
print("=" * 50)
print(f"Customers      : {len(customers)}")
print(f"Accounts       : {len(accounts)}")
print(f"Transactions   : {len(transactions)}")
print(f"Loans          : {len(loans)}")
print(f"EMI records    : {len(emi_records)}")
print(f"Fraud events   : {len(fraud_events)}")
print(f"Products       : {len(products)}")
print(f"Events         : {len(events)}")
print("=" * 50)
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

NUM_CUSTOMERS = 100
TRANSACTIONS_PER_CUSTOMER = 60


FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rahul",
    "Rohan", "Vikram", "Karan", "Akash", "Nikhil",
    "Ananya", "Priya", "Isha", "Kavya", "Sneha",
    "Meera", "Pooja", "Riya", "Neha", "Diya",
]

LAST_NAMES = [
    "Sharma", "Patel", "Mehta", "Shah", "Verma",
    "Gupta", "Joshi", "Desai", "Singh", "Kumar",
]

CITIES = [
    "Ahmedabad",
    "Gandhinagar",
    "Mumbai",
    "Pune",
    "Bengaluru",
    "Delhi",
    "Jaipur",
    "Surat",
    "Vadodara",
    "Hyderabad",
]

OCCUPATIONS = [
    "Software Engineer",
    "Teacher",
    "Business Owner",
    "Doctor",
    "Accountant",
    "Designer",
    "Marketing Manager",
    "Government Employee",
    "Consultant",
    "Student",
]

MERCHANTS = [
    ("Amazon", "Shopping"),
    ("Flipkart", "Shopping"),
    ("Swiggy", "Food"),
    ("Zomato", "Food"),
    ("Uber", "Transport"),
    ("Ola", "Transport"),
    ("BigBasket", "Groceries"),
    ("Reliance Fresh", "Groceries"),
    ("Netflix", "Entertainment"),
    ("BookMyShow", "Entertainment"),
    ("Apollo Pharmacy", "Healthcare"),
    ("Electricity Board", "Utilities"),
    ("Airtel", "Utilities"),
    ("Jio", "Utilities"),
]

LOAN_TYPES = [
    "Personal Loan",
    "Home Loan",
    "Education Loan",
    "Vehicle Loan",
]

TRANSACTION_TYPES = [
    "DEBIT",
    "DEBIT",
    "DEBIT",
    "CREDIT",
]


# ============================================================
# CUSTOMERS
# ============================================================

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    name = f"{first} {last}"

    email = (
        f"{first.lower()}.{last.lower()}"
        f"{customer_id}@finguru.demo"
    )

    monthly_income = round(
        random.uniform(25000, 180000),
        2,
    )

    customers.append(
        {
            "id": customer_id,
            "customer_code": f"FG{customer_id:05d}",
            "full_name": name,
            "email": email,
            "phone": f"9{random.randint(100000000, 999999999)}",
            "date_of_birth": (
                datetime(
                    random.randint(1970, 2002),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ).date()
            ),
            "city": random.choice(CITIES),
            "occupation": random.choice(OCCUPATIONS),
            "monthly_income": monthly_income,
        }
    )


pd.DataFrame(customers).to_csv(
    DATA_DIR / "customers.csv",
    index=False,
)


# ============================================================
# ACCOUNTS
# ============================================================

accounts = []

for customer in customers:

    customer_id = customer["id"]

    balance = round(
        customer["monthly_income"]
        * random.uniform(0.8, 4.0),
        2,
    )

    accounts.append(
        {
            "id": customer_id,
            "customer_id": customer_id,
            "account_number": f"FGSB{customer_id:010d}",
            "account_type": "savings",
            "balance": balance,
            "currency": "INR",
            "status": "active",
        }
    )


pd.DataFrame(accounts).to_csv(
    DATA_DIR / "accounts.csv",
    index=False,
)


# ============================================================
# TRANSACTIONS
# ============================================================

transactions = []

transaction_id = 1

today = datetime.utcnow()

for customer in customers:

    customer_id = customer["id"]
    income = customer["monthly_income"]

    account_id = customer_id

    # Salary transaction
    transactions.append(
        {
            "id": transaction_id,
            "customer_id": customer_id,
            "account_id": account_id,
            "transaction_type": "CREDIT",
            "amount": income,
            "merchant": "Employer",
            "category": "Salary",
            "location": customer["city"],
            "device_id": f"DEVICE_{customer_id:04d}",
            "beneficiary": None,
            "description": "Monthly salary credit",
            "timestamp": (
                today
                - timedelta(days=random.randint(0, 25))
            ).isoformat(),
        }
    )

    transaction_id += 1

    for _ in range(TRANSACTIONS_PER_CUSTOMER):

        merchant, category = random.choice(MERCHANTS)

        amount = round(
            random.uniform(200, income * 0.08),
            2,
        )

        transactions.append(
            {
                "id": transaction_id,
                "customer_id": customer_id,
                "account_id": account_id,
                "transaction_type": "DEBIT",
                "amount": amount,
                "merchant": merchant,
                "category": category,
                "location": customer["city"],
                "device_id": f"DEVICE_{customer_id:04d}",
                "beneficiary": None,
                "description": f"{category} transaction",
                "timestamp": (
                    today
                    - timedelta(
                        days=random.randint(0, 180)
                    )
                ).isoformat(),
            }
        )

        transaction_id += 1


pd.DataFrame(transactions).to_csv(
    DATA_DIR / "transactions.csv",
    index=False,
)


# ============================================================
# LOANS
# ============================================================

loans = []
loan_id = 1

for customer in customers:

    if random.random() < 0.45:

        principal = round(
            random.uniform(50000, 800000),
            2,
        )

        interest_rate = round(
            random.uniform(8.5, 15.5),
            2,
        )

        tenure = random.choice(
            [12, 24, 36, 48, 60]
        )

        monthly_rate = interest_rate / 12 / 100

        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** tenure
            / (
                (1 + monthly_rate) ** tenure - 1
            )
        )

        outstanding = round(
            principal * random.uniform(0.35, 1.0),
            2,
        )

        loans.append(
            {
                "id": loan_id,
                "customer_id": customer["id"],
                "loan_type": random.choice(LOAN_TYPES),
                "principal_amount": principal,
                "interest_rate": interest_rate,
                "tenure_months": tenure,
                "monthly_emi": round(emi, 2),
                "outstanding_amount": outstanding,
                "status": "active",
            }
        )

        loan_id += 1


pd.DataFrame(loans).to_csv(
    DATA_DIR / "loans.csv",
    index=False,
)


# ============================================================
# EMI RECORDS
# ============================================================

emi_records = []

emi_id = 1

for loan in loans:

    for month in range(1, 7):

        due_date = (
            datetime.utcnow()
            - timedelta(days=30 * (6 - month))
        ).date()

        status = random.choices(
            ["paid", "pending", "missed"],
            weights=[0.82, 0.12, 0.06],
        )[0]

        paid_amount = (
            loan["monthly_emi"]
            if status == "paid"
            else 0
        )

        emi_records.append(
            {
                "id": emi_id,
                "loan_id": loan["id"],
                "customer_id": loan["customer_id"],
                "due_date": due_date.isoformat(),
                "amount": loan["monthly_emi"],
                "paid_amount": paid_amount,
                "status": status,
                "paid_at": (
                    due_date.isoformat()
                    if status == "paid"
                    else None
                ),
            }
        )

        emi_id += 1


pd.DataFrame(emi_records).to_csv(
    DATA_DIR / "emi_records.csv",
    index=False,
)


# ============================================================
# FRAUD EVENTS
# ============================================================

fraud_events = []

fraud_id = 1

for _ in range(30):

    customer = random.choice(customers)

    score = round(
        random.uniform(0.65, 0.99),
        3,
    )

    fraud_events.append(
        {
            "id": fraud_id,
            "customer_id": customer["id"],
            "transaction_id": None,
            "fraud_score": score,
            "risk_level": (
                "HIGH"
                if score >= 0.8
                else "MEDIUM"
            ),
            "status": "open",
            "reason": random.choice(
                [
                    "Unusual transaction amount",
                    "New device detected",
                    "Unusual location",
                    "High transaction frequency",
                    "New beneficiary",
                ]
            ),
            "anomaly_score": round(
                random.uniform(0.6, 1.0),
                3,
            ),
            "rule_score": round(
                random.uniform(0.5, 1.0),
                3,
            ),
            "identity_risk_score": round(
                random.uniform(0.2, 0.9),
                3,
            ),
            "recommended_action": "VERIFY_TRANSACTION",
        }
    )

    fraud_id += 1


pd.DataFrame(fraud_events).to_csv(
    DATA_DIR / "fraud_events.csv",
    index=False,
)


# ============================================================
# PRODUCTS
# ============================================================

products = [
    {
        "product_code": "PL001",
        "name": "Personal Loan",
        "product_type": "loan",
        "description": "Flexible personal loan for eligible customers.",
        "interest_rate": 11.5,
        "min_amount": 50000,
        "max_amount": 1000000,
        "active": True,
    },
    {
        "product_code": "HL001",
        "name": "Home Loan",
        "product_type": "loan",
        "description": "Home financing solution.",
        "interest_rate": 8.5,
        "min_amount": 500000,
        "max_amount": 10000000,
        "active": True,
    },
    {
        "product_code": "FD001",
        "name": "Fixed Deposit",
        "product_type": "investment",
        "description": "Fixed deposit savings product.",
        "interest_rate": 7.0,
        "min_amount": 1000,
        "max_amount": 10000000,
        "active": True,
    },
    {
        "product_code": "RD001",
        "name": "Recurring Deposit",
        "product_type": "investment",
        "description": "Monthly recurring savings product.",
        "interest_rate": 6.5,
        "min_amount": 500,
        "max_amount": 1000000,
        "active": True,
    },
]


with open(
    DATA_DIR / "products.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        products,
        file,
        indent=2,
    )


# ============================================================
# EVENTS
# ============================================================

events = [
    {
        "event_type": "SALARY_CREDITED",
        "description": "Monthly salary credited",
    },
    {
        "event_type": "EMI_DUE",
        "description": "Loan EMI due",
    },
    {
        "event_type": "EMI_MISSED",
        "description": "Loan EMI missed",
    },
    {
        "event_type": "LARGE_TRANSACTION",
        "description": "Large transaction detected",
    },
    {
        "event_type": "NEW_DEVICE",
        "description": "New device detected",
    },
    {
        "event_type": "NEW_BENEFICIARY",
        "description": "New beneficiary added",
    },
    {
        "event_type": "SPENDING_SPIKE",
        "description": "Spending spike detected",
    },
    {
        "event_type": "BALANCE_DROP",
        "description": "Significant balance drop detected",
    },
]


with open(
    DATA_DIR / "events.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        events,
        file,
        indent=2,
    )


# ============================================================
# SUMMARY
# ============================================================

print("\nFinGuru synthetic banking dataset generated.")
print("=" * 50)
print(f"Customers      : {len(customers)}")
print(f"Accounts       : {len(accounts)}")
print(f"Transactions   : {len(transactions)}")
print(f"Loans          : {len(loans)}")
print(f"EMI records    : {len(emi_records)}")
print(f"Fraud events   : {len(fraud_events)}")
print(f"Products       : {len(products)}")
print(f"Events         : {len(events)}")
print("=" * 50)
