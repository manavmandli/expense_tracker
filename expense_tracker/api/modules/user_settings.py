import frappe
from frappe import _
from expense_tracker.api.models import UserSettingModel
from expense_tracker.api.api_utils import remove_default_fields


class UserSetting:
    def __init__(self):
        self.user = frappe.session.user

    def get_user_settings(self):
        """Retrieve all user setting details"""
        user_setting = remove_default_fields(
            frappe.get_all(
                "User Settings",
                filters={"name": frappe.session.user},
                fields=[
                    "*",
                ],
            )
        )
        frappe.response["message"] = "User Settings Details get successfully"
        return user_setting

    def update_user_settings(self, data: UserSettingModel):
        """Update user settings details"""
        user_setting_doc = frappe.get_doc("User Settings", frappe.session.user)

        user_setting_doc.currency = data.currency
        user_setting_doc.country = data.country
        user_setting_doc.amount_format = data.amount_format

        user_setting_doc.save(ignore_permissions=True)
        frappe.response["message"] = "User Settings Updated Successfully"
        frappe.response["name"] = user_setting_doc.name
