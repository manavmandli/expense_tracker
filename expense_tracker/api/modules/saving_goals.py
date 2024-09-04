import frappe
from frappe import _
from expense_tracker.api.models import SavingGoalsModel


class SavingGoal:
    def __init__(self):
        self.user = frappe.session.user

    def get_saving_goals():
        pass

    def create_saving_goals():
        pass

    def update_saving_goals():
        pass
