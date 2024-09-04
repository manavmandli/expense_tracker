import frappe
from frappe import _
from expense_tracker.api.models import UserSettingModel


class UserSetting:
    def __init__(self):
        self.user = frappe.session.user

    def get_user_settings():
        pass

    def update_user_settings():
        pass
