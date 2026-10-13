import pandas as pd

REPORT_DATE = pd.Timestamp("2026-10-14")
INACTIVE_DAYS = 90

accounts = pd.read_csv("data/accounts.csv")
accounts["last_login"] = pd.to_datetime(accounts["last_login"])

accounts["days_since_login"] = (REPORT_DATE - accounts["last_login"]).dt.days
not_logged_in_recently = accounts["days_since_login"] > INACTIVE_DAYS
is_active = accounts["status"] == "active"
inactive = accounts[not_logged_in_recently & is_active]

# ---- Check 2: the same email used more than once ----
duplicates = accounts[accounts["email"].duplicated(keep=False)].sort_values("email")

# ---- Check 3: disabled accounts that still hold a license ----
is_disabled = accounts["status"] == "disabled"
has_license = accounts["license"].notna()
wasted_licenses = accounts[is_disabled & has_license]

print(wasted_licenses)
print(len(wasted_licenses))