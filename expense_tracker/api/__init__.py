import frappe
from expense_tracker.api.auth import Auth
from expense_tracker.api.modules import (
    log,
    get_budget,
    update_budget,
    create_budget,
    get_saving_goals,
    create_saving_goals,
    update_saving_goals,
    get_transaction,
    update_transaction,
    create_saving_transaction,
    create_transaction,
    create_transfer_transaction,
    get_user_profile,
    update_user_profile,
    get_user_settings,
    update_user_settings,
)
from expense_tracker.api.models import (
    UserModel,
    CategoryModel,
    UserAccountModel,
    BudgetModel,
    SavingGoalsModel,
    SavingTransactionModel,
    TransactionModel,
    TransferTransactionModel,
    UserSetting,
)
from expense_tracker.api.masters import (
    get_category,
    create_category,
    get_user_accounts,
    create_user_account,
)
from bs4 import BeautifulSoup


endpoints = {
    # Auth End Points
    "login": {
        "methods": {"POST"},
        "function": Auth().login,
    },
    "signup": {
        "methods": {"POST"},
        "function": Auth().create_account,
        "model": UserModel,
    },
    # Category End Points
    "get_category": {
        "methods": {"GET"},
        "function": get_category,
    },
    "create_category": {
        "methods": {"POST"},
        "function": create_category,
        "model": CategoryModel,
    },
    # User Account End Points
    "get_user_accounts": {
        "methods": {"GET"},
        "function": get_user_accounts,
    },
    "create_user_account": {
        "methods": {"POST"},
        "function": create_user_account,
        "model": UserAccountModel,
    },
    # Budget End Points
    "get_budget": {
        "methods": {"GET"},
        "function": get_budget,
    },
    "update_budget": {
        "methods": {"PUT"},
        "function": update_budget,
        "model": BudgetModel,
    },
    "create_budget": {
        "methods": {"POST"},
        "function": create_budget,
        "model": BudgetModel,
    },
    # Saving End Points
    "get_saving_goals": {
        "methods": {"GET"},
        "function": get_saving_goals,
    },
    "create_saving_goals": {
        "methods": {"POST"},
        "function": create_saving_goals,
        "model": SavingGoalsModel,
    },
    "update_saving_goals": {
        "methods": {"PUT"},
        "function": update_saving_goals,
        "model": SavingGoalsModel,
    },
    # Transaction End-Points
    "get_transaction": {
        "methods": {"GET"},
        "function": get_transaction,
    },
    "update_transaction": {
        "methods": {"PUT"},
        "function": update_transaction,
        # "model": SavingGoalsModel,(pending due to confusion)
    },
    "create_saving_transaction": {
        "methods": {"POST"},
        "function": create_saving_transaction,
        "model": SavingTransactionModel,
    },
    "create_transaction": {
        "methods": {"POST"},
        "function": create_transaction,
        "model": TransactionModel,
    },
    "create_transfer_transaction": {
        "methods": {"POST"},
        "function": create_transfer_transaction,
        "model": TransferTransactionModel,
    },
    # User Profile End Points
    "get_user_profile": {
        "methods": {"GET"},
        "function": get_user_profile,
    },
    "update_user_profile": {
        "methods": {"PUT"},
        "function": update_user_profile,
        "model": UserModel,
    },
    # User Settings End Points
    "get_user_settings": {
        "methods": {"GET"},
        "function": get_user_settings,
    },
    "update_user_settings": {
        "methods": {"PUT"},
        "function": update_user_settings,
        "model": UserSetting,
    },
}


@frappe.whitelist(methods=["POST", "GET", "PUT", "DELETE"], allow_guest=True)
@log()
def v1(type: str, data: dict | None = None, **kwargs):
    """
    data param is for POST and should be converted to Pydantic Model
    """
    endpoint = endpoints.get(type)

    if not endpoint:
        gen_response(404, "Endpoint not found.")
        return

    if frappe.request.method not in endpoint["methods"]:
        gen_response(405, "Method not allowed.")
        return

    if not data:
        data = dict()

    model = endpoint.get("model")
    if model:
        data = model(**data)

    try:
        if frappe.request.method == "POST":
            frappe.db.begin()

        if not model:
            result = endpoint["function"](**data)
        else:
            result = endpoint["function"](data)

        if frappe.request.method == "POST":
            frappe.db.commit()
    except frappe.AuthenticationError:
        return gen_response(500, frappe.response["message"])
    except Exception as e:
        frappe.log_error(title="Expense Tracker Error", message=frappe.get_traceback())
        result = str(e)
        return gen_response(500, result)
    finally:
        if frappe.request.method == "POST":
            frappe.db.close()

    gen_response(
        200,
        frappe.response["message"],
        result,
    )
    return


def gen_response(status, message, data=None):
    frappe.response["http_status_code"] = status
    if status == 500:
        frappe.response["message"] = BeautifulSoup(str(message)).get_text()
    else:
        frappe.response["message"] = message
    if data is not None:
        frappe.response["data"] = data
