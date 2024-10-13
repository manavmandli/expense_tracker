import frappe
from expense_tracker.api.auth import Auth
from expense_tracker.api.modules import (
    log,
    Budget,
    SavingGoal,
    Transaction,
    UserProfile,
    UserSetting,
)
from expense_tracker.api.models import (
    UserModel,
    UserProfileModel,
    ForgetPwdModel,
    CategoryModel,
    UserAccountModel,
    BudgetModel,
    SavingGoalsModel,
    SavingTransactionModel,
    TransactionModel,
    TransferTransactionModel,
    UserSettingModel,
)
from expense_tracker.api.masters import Category, UserAccount
from bs4 import BeautifulSoup


endpoints = {
    # Auth End Points
    "login": {"methods": {"POST"}, "function": Auth().login, "allow_guest": True},
    "signup": {
        "methods": {"POST"},
        "function": Auth().create_account,
        "model": UserModel,
        "allow_guest": True,
    },
    "send_otp": {"methods": {"POST"}, "function": Auth().send_otp, "allow_guest": True},
    "validate_otp": {
        "methods": {"POST"},
        "function": Auth().validate_otp,
        "model": ForgetPwdModel,
        "allow_guest": True,
    },
    "logout": {"methods": {"POST"}, "function": Auth().logout, "allow_guest": False},
    # Category End Points
    "get_category": {
        "methods": {"GET"},
        "function": Category().get_category,
        "allow_guest": True,
    },
    "create_category": {
        "methods": {"POST"},
        "function": Category().create_category,
        "model": CategoryModel,
        "allow_guest": False,
    },
    # User Account End Points
    "get_user_accounts": {
        "methods": {"GET"},
        "function": UserAccount().get_user_accounts,
        "allow_guest": False,
    },
    "update_user_account": {
        "methods": {"POST"},
        "function": UserAccount().update_user_account,
        "allow_guest": False,
    },
    "create_user_account": {
        "methods": {"POST"},
        "function": UserAccount().create_user_account,
        "model": UserAccountModel,
        "allow_guest": False,
    },
    # Budget End Points
    "get_budget": {
        "methods": {"GET"},
        "function": Budget().get_budget,
        "allow_guest": False,
    },
    "update_budget": {
        "methods": {"PUT"},
        "function": Budget().update_budget,
        "allow_guest": False,
    },
    "create_budget": {
        "methods": {"POST"},
        "function": Budget().create_budget,
        "model": BudgetModel,
        "allow_guest": False,
    },
    # Saving End Points
    "get_saving_goals": {
        "methods": {"GET"},
        "function": SavingGoal().get_saving_goals,
        "allow_guest": False,
    },
    "create_saving_goals": {
        "methods": {"POST"},
        "function": SavingGoal().create_saving_goals,
        "model": SavingGoalsModel,
        "allow_guest": False,
    },
    "update_saving_goals": {
        "methods": {"PUT"},
        "function": SavingGoal().update_saving_goals,
        "allow_guest": False,
    },
    # Transaction End-Points
    "get_transaction": {
        "methods": {"GET"},
        "function": Transaction().get_transaction,
        "allow_guest": False,
    },
    "update_transaction": {
        "methods": {"PUT"},
        "function": Transaction().update_transaction,
        # "model": SavingGoalsModel,(pending due to confusion)
        "allow_guest": False,
    },
    "create_saving_transaction": {
        "methods": {"POST"},
        "function": Transaction().create_saving_transaction,
        "model": SavingTransactionModel,
        "allow_guest": False,
    },
    "create_transaction": {
        "methods": {"POST"},
        "function": Transaction().create_transaction,
        "model": TransactionModel,
        "allow_guest": False,
    },
    "create_transfer_transaction": {
        "methods": {"POST"},
        "function": Transaction().create_transfer_transaction,
        "model": TransferTransactionModel,
        "allow_guest": False,
    },
    # User Profile End Points
    "get_user_profile": {
        "methods": {"GET"},
        "function": UserProfile().get_user_profile,
        "allow_guest": False,
    },
    "update_user_profile": {
        "methods": {"PUT"},
        "function": UserProfile().update_user_profile,
        "model": UserProfileModel,
        "allow_guest": False,
    },
    # User Settings End Points
    "get_user_settings": {
        "methods": {"GET"},
        "function": UserSetting().get_user_settings,
        "allow_guest": False,
    },
    "update_user_settings": {
        "methods": {"PUT"},
        "function": UserSetting().update_user_settings,
        "model": UserSettingModel,
        "allow_guest": False,
    },
}


def get_allow_guest(type: str):
    endpoint = endpoints.get(type)
    return endpoint.get("allow_guest", False) if endpoint else False


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

    allow_guest = get_allow_guest(type)
    if not allow_guest and frappe.session.user == "Guest":
        gen_response(403, "Guest access not allowed for this endpoint.")
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
