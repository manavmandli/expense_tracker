import frappe
from frappe import _
from expense_tracker.api.models import UserModel, ForgetPwdModel
from frappe.sessions import clear_sessions


class Auth:
    def __init__(self, name=None, mobile_no=None, email=None) -> None:
        self.user = frappe.session.user
        self.name = name
        self.mobile_no = mobile_no
        self.email = email

    def validate_duplicate(self):
        if frappe.db.exists("User", {"username": self.name}):
            frappe.throw(_("Username already exists"))
        if frappe.db.exists("User", {"email": self.email}):
            frappe.throw(_("Email already exists"))
        if frappe.db.exists("User", {"mobile_no": self.mobile_no}):
            frappe.throw(_("Mobile no already exists"))

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
        self.create_user_settings(data.email)
        frappe.response["message"] = "Account created successfully"
        frappe.response["user"] = data.name

    def create_user_settings(self,email):
        user_settiing_doc = frappe.get_doc(
            dict(
                doctype="User Settings",
                user=email
            )
        )
        user_settiing_doc.insert(ignore_permissions=True)

    def login(self, usr, pwd):
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        self.user = frappe.session.user
        if frappe.response.get("message") == "Logged In":
            frappe.response["user"] = self.user
            frappe.response["key_details"] = self.generate_key(login_manager.user)

    def logout(self):
        if frappe.session.user == "Guest":
            frappe.throw(_("Login is Required for Logout"))
        frappe.local.login_manager.logout()
        clear_sessions(frappe.session.user, keep_current=False, force=True)
        frappe.response["message"] = _("Successfully logged out.")

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

    def id_generator_otp(self):
        return "123456"

    def send_otp(self, mobile_no):
        if not mobile_no:
            frappe.throw(_("Mobile No is required"))

        if not frappe.db.exists("User", {"mobile_no": mobile_no}):
            frappe.throw(_("Mobile no. Not exists"))

        user_otp_doc = frappe.db.exists("User OTP", {"mobile_no": mobile_no})
        if user_otp_doc:
            frappe.db.sql("""delete from `tabUser OTP` where mobile_no=%s""", mobile_no)
        otp_code = self.id_generator_otp()
        frappe.response["message"] = "OTP Sent on registered mobile no"
        userOTP = frappe.get_doc(
            dict(doctype="User OTP", mobile_no=mobile_no, otp=otp_code)
        ).insert(ignore_permissions=True)

    def validate_otp(self, data: ForgetPwdModel):
        otp_exists = frappe.db.exists(
            "User OTP", {"mobile_no": data.mobile_no, "otp": data.otp}
        )
        if not otp_exists:
            frappe.throw(_("Invalid OTP"))

        user_doc = frappe.get_doc("User", {"mobile_no": data.mobile_no})

        if not data.new_password:
            frappe.throw(_("Password can not be blank"))

        user_doc.new_password = data.new_password
        user_doc.save(ignore_permissions=True)

        frappe.response["message"] = "Password Updated Successfully"
