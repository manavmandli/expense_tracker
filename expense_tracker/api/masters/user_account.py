import frappe
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import UserAccountModel


def get_user_accounts():
    """Retrieve all User Accounts."""

    user_account_doc = remove_default_fields(
        frappe.get_all(
            "User Account", filters={"user": frappe.session.user}, fields=["*"]
        )
    )
    frappe.response["message"] = "User Account list get successfully"
    return user_account_doc


def create_user_account(data: UserAccountModel):
    """Create a new User Account"""

    if data.account_type in ["Bank", "Other"]:
        user_account_doc = frappe.get_doc(
            dict(
                doctype="User Account",
                user=frappe.session.user,
                account_type=data.account_type,
                account_name=data.account_name,
                opening_balance=data.opening_balance,
                receivable=data.receivable,
                payable=data.payable,
            )
        )
        user_account_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "User Account created successfully"
    else:
        frappe.response["message"] = "Invalid Account Type"
