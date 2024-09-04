import frappe
from frappe import _
from expense_tracker.api.models import BudgetModel


class Budget:
    def __init__(self):
        self.user = frappe.session.user

    def get_budget():
        pass

    def create_budget(data: BudgetModel):
        pass

    def update_budget():
        pass
