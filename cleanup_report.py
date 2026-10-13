from pathlib import Path

import pandas as pd

# ---- Settings ----
REPORT_DATE = pd.Timestamp("2026-10-14")
INACTIVE_DAYS = 90
OUTPUT_DIR = Path("output")

# ---- Load the data ----
accounts = pd.read_csv("data/accounts.csv")
accounts["last_login"] = pd.to_datetime(accounts["last_login"])
accounts["days_since_login"] = (REPORT_DATE - accounts["last_login"]).dt.days

# ---- Check 1: active accounts not used for over 90 days ----
not_logged_in_recently = accounts["days_since_login"] > INACTIVE_DAYS
is_active = accounts["status"] == "active"
inactive = accounts[not_logged_in_recently & is_active]

# ---- Check 2: the same email used more than once ----
duplicates = accounts[accounts["email"].duplicated(keep=False)].sort_values("email")

# ---- Check 3: disabled accounts that still hold a license ----
is_disabled = accounts["status"] == "disabled"
has_license = accounts["license"].notna()
wasted_licenses = accounts[is_disabled & has_license]

# ---- Build the cleaned list ----
# Keep the most recent login for each email, so duplicates are removed
cleaned = accounts.sort_values("last_login", ascending=False)
cleaned = cleaned.drop_duplicates(subset="email", keep="first")

# Take licenses back from disabled accounts
cleaned.loc[cleaned["status"] == "disabled", "license"] = pd.NA

# Flag inactive accounts for a person to review (not deleted automatically)
cleaned["needs_review"] = (cleaned["days_since_login"] > INACTIVE_DAYS) & (
    cleaned["status"] == "active"
)
cleaned = cleaned.sort_values("name")

# ---- Save the cleaned CSV ----
OUTPUT_DIR.mkdir(exist_ok=True)
cleaned.to_csv(OUTPUT_DIR / "cleaned_accounts.csv", index=False)
print(f"Saved {len(cleaned)} accounts to {OUTPUT_DIR / 'cleaned_accounts.csv'}")