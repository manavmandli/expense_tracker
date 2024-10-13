import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import UserProfileModel


class UserProfile:
    def __init__(self):
        self.user = frappe.session.user

    def get_user_profile(self):
        """Retrieve all profile details"""
        user_profile = remove_default_fields(
            frappe.get_all(
                "User",
                filters={"name": frappe.session.user},
                fields=[
                    "user_image",
                    "full_name",
                    "email",
                    "mobile_no",
                    "birth_date",
                    "gender",
                ],
            )
        )
        frappe.response["message"] = "User Profile Details get successfully"
        return user_profile

    def update_user_profile(self, data: UserProfileModel):
        """Update user profile details"""
        user_doc = frappe.get_doc("User", frappe.session.user)

        if frappe.db.exists("User", {"mobile_no": data.mobile_no}):
            frappe.throw(_("Mobile no already exists"))

        user_doc.first_name = data.name
        user_doc.mobile_no = data.mobile_no
        user_doc.birth_date = data.dob
        user_doc.gender = data.gender

        user_doc.save(ignore_permissions=True)
        frappe.response["message"] = "User Profile Updated Successfully"
        frappe.response["name"] = user_doc.name
