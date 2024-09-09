import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import CategoryModel


class Category:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def get_category():
        """Retrieve all categories."""

        categories = remove_default_fields(
            frappe.get_all(
                "Category", filters={"owner": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Category list get successfully"
        return categories

    def create_category(data: CategoryModel):
        """Create a new category with optional icon upload."""

        if data.category_type in ["Expense", "Income", "Transfer"]:
            category_doc = frappe.get_doc(
                dict(
                    doctype="Category",
                    category_name=data.category_name,
                    category_type=data.category_type,
                )
            )
            category_doc.insert(ignore_permissions=True)
            frappe.response["message"] = (
                f"{category_doc.name} Category created successfully"
            )
        else:
            frappe.response["message"] = "Invalid category type"
