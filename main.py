import csv
from pathlib import Path
import matplotlib.pyplot as plt

DATA_FILE = Path("data") / "customers.csv"


customers = []

with DATA_FILE.open() as file:
    lines = file.readlines()

if not lines:
    raise ValueError("customers.csv is empty or not found")


header = lines[0].strip().split(",")

for line in lines[1:]:
    values = line.strip().split(",")
    customer = dict(zip(header, values))

    customer["customer_id"] = int(customer["customer_id"])
    customer["total_spent"] = int(customer["total_spent"])
    customer["purchases"] = int(customer["purchases"])
    customer["last_purchase_days_ago"] = int(
        customer["last_purchase_days_ago"])

    customers.append(customer)

print(customers)

# -----------------------------step 2a----------------------------


def segment_customer(customer):
    if customer["total_spent"] >= 1000:
        return "VIP"
    elif customer["purchases"] >= 10:
        return "Loyal"
    elif customer["last_purchase_days_ago"] >= 180:
        return "Lost"
    elif customer["last_purchase_days_ago"] >= 60:
        return "At Risk"
    else:
        return "Regular"


# -----------------------------step 2b----------------------------
for customer in customers:
    segment = segment_customer(customer)
    customer["segment"] = segment

# -----------------------------step 2c----------------------------

for customer in customers:
    print(f"Customer {customer['customer_id']} → {customer["segment"]}"
          )

# -----------------------------step 3a----------------------------


def retention_status(customer):
    days = customer["last_purchase_days_ago"]

    if days < 30:
        return "Active"
    elif days < 90:
        return "At Risk"
    else:
        return "Lost"

# -----------------------------step 3b----------------------------


retention_summary = {
    "Active": 0,
    "At Risk": 0,
    "Lost": 0
}

for customer in customers:
    status = retention_status(customer)
    retention_summary[status] += 1

# -----------------------------step 3c----------------------------

print("\nRetention Summary:")
for status, count in retention_summary.items():
    print(f"{status}: {count}")

# -----------------------------step 4c -A----------------------------


def recommend_action(customer):
    segment = customer["segment"]
    retention = retention_status(customer)

    if segment == "VIP" and retention == "Active":
        return "Send personal thank-you and perks"
    elif segment == "VIP" and retention == "At Risk":
        return "Send exclusive VIP offer"
    elif segment == "Loyal" and retention == "Active":
        return "Give loyalty reward"
    elif segment == "Loyal" and retention == "At Risk":
        return "Send discount reminder"
    elif segment == "Regular" and retention == "Active":
        return "Upsell related products"
    elif segment == "Regular" and retention == "At Risk":
        return "Send re-engagement email"
    elif segment == "Lost":
        return "Win-back campaign"
    else:
        return "Reminder with small discount"

# -----------------------------step 4c -b----------------------------


for customer in customers:
    customer["action"] = recommend_action(customer)

# -----------------------------step 4c -c----------------------------

print("\nCustomer Action Report:")
for c in customers:
    print(
        f"Customer {c['customer_id']} | "
        f"Segment: {c['segment']} | "
        f"Status: {retention_status(c)} | "
        f"Action: {c['action']}"
    )


# -----------------------------step 5b -a----------------------------

total_customers = len(customers)

segment_counts = {}
retention_counts = {
    "Active": 0,
    "At Risk": 0,
    "Lost": 0
}

for customer in customers:
    # Segment counts
    seg = customer["segment"]
    segment_counts[seg] = segment_counts.get(seg, 0) + 1

    # Retention counts
    status = retention_status(customer)
    retention_counts[status] += 1

# -----------------------------step 5b -b----------------------------

vip_percentage = (segment_counts.get("VIP", 0) / total_customers) * 100
churn_rate = (retention_counts["Lost"] / total_customers) * 100
retention_rate = (
    (retention_counts["Active"] + retention_counts["At Risk"])
    / total_customers
) * 100
at_risk_rate = (retention_counts["At Risk"] / total_customers) * 100

# -----------------------------step 5b -c----------------------------

print("\n--- KPI DASHBOARD ---")
print(f"Total customers: {total_customers}")
print(f"VIP percentage: {vip_percentage:.2f}%")
print(f"Retention rate: {retention_rate:.2f}%")
print(f"At-risk rate: {at_risk_rate:.2f}%")
print(f"Churn rate: {churn_rate:.2f}%")


# -----------------------------export to csv file---------------------


with open("customers_report.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "customer_id",
        "segment",
        "retention_status",
        "action"
    ])

    # Rows
    for c in customers:
        writer.writerow([
            c["customer_id"],
            c["segment"],
            retention_status(c),
            c["action"]
        ])

with open("kpis.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["metric", "value"])
    writer.writerow(["Total customers", total_customers])
    writer.writerow(["VIP percentage", f"{vip_percentage:.2f}%"])
    writer.writerow(["Retention rate", f"{retention_rate:.2f}%"])
    writer.writerow(["At-risk rate", f"{at_risk_rate:.2f}%"])
    writer.writerow(["Churn rate", f"{churn_rate:.2f}%"])

# ------------------------------PLOTS----------------------------
segments = list(segment_counts.keys())
counts = list(segment_counts.values())

plt.figure()
plt.bar(segments, counts)
plt.title("Customers by Segment")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.show()


statuses = list(retention_counts.keys())
status_values = list(retention_counts.values())

plt.figure()
plt.pie(
    status_values,
    labels=statuses,
    autopct="%1.1f%%"
)
plt.title("Customer Retention Status")
plt.show()

kpi_names = ["Retention", "At Risk", "Churn"]
kpi_values = [retention_rate, at_risk_rate, churn_rate]

plt.figure()
plt.bar(kpi_names, kpi_values)
plt.ylabel("Percentage")
plt.title("Key Retention Metrics")
plt.show()
