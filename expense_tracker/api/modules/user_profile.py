import frappe
from frappe import _
from expense_tracker.api.models import UserModel


class UserProfile:
    def __init__(self):
        self.user = frappe.session.user

    def get_user_profile():
        pass

    def update_user_profile():
        pass
