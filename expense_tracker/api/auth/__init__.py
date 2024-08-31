import frappe
from frappe import _
from expense_tracker.api.models import UserModel


class Auth:
    def __init__(self, name=None, mobile_no=None, email=None) -> None:
        self.user = frappe.session.user
        self.name = name
        self.mobile_no = mobile_no
        self.email = email

    def get_user_detail(self):
        return frappe.db.get_value(
            "User",
            {"full_name": self.name, "mobile_no": self.mobile_no, "email": self.email},
            "name",
        )

    def validate_duplicate(self):
        if self.get_user_detail():
            frappe.throw(_("User already exists"))

    def create_account(self, data: UserModel):
        # Setting the instance attributes for use in get_user_detail
        self.name = data.name
        self.mobile_no = data.mobile_no
        self.email = data.email

        self.validate_duplicate()

        user_doc = frappe.get_doc(
            dict(
                doctype="User",
                first_name=data.name,
                email=data.email,
                mobile_no=data.mobile_no,
                new_password=data.password,
                roles=[
                    {
                        "doctype": "Has Role",
                        "parentfield": "roles",
                        "role": "System Manager",
                    }
                ],
            )
        )
        user_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "Account created successfully"
        frappe.response["user"] = data.name

    def login(self, usr, pwd):
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        self.user = frappe.session.user
        if frappe.response.get("message") == "Logged In":
            frappe.response["user"] = self.user
            frappe.response["key_details"] = self.generate_key(login_manager.user)

    def generate_key(self, user):
        user_details = frappe.get_doc("User", user)
        api_secret = api_key = ""
        if not user_details.api_key and not user_details.api_secret:
            api_secret = frappe.generate_hash(length=15)
            api_key = frappe.generate_hash(length=15)
            user_details.api_key = api_key
            user_details.api_secret = api_secret
            user_details.save(ignore_permissions=True)
        else:
            api_secret = user_details.get_password("api_secret")
            api_key = user_details.get("api_key")
        return {"api_secret": api_secret, "api_key": api_key}
