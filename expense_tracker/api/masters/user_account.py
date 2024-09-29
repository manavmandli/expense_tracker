import frappe
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import UserAccountModel


class UserAccount:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def get_user_accounts(self):
        """Retrieve all User Accounts."""
        user_account_doc = remove_default_fields(
            frappe.get_all(
                "User Account", filters={"user": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "User Account list get successfully"
        return user_account_doc
    
    def update_user_account(self, **data):
        """Update an existing User Account"""
        user_account_doc = frappe.get_doc("User Account", data.get("account"))
        
        if data.get("account_type") and data.get("account_type") in ["Bank", "Other"]:
            user_account_doc.account_type = data.get("account_type")
        if data.get("account_name"):
            user_account_doc.account_name = data.get("account_name")
            
        user_account_doc.save(ignore_permissions=True)
        frappe.response["message"] = "User Account updated successfully"

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
