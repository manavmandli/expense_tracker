from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    email: str
    mobile_no: str
    password: str


class UserProfileModel(BaseModel):
    name: str
    mobile_no:str
    dob: str
    gender: str


class ForgetPwdModel(BaseModel):
    mobile_no: str
    otp: str
    new_password: str


class CategoryModel(BaseModel):
    category_name: str
    category_type: str


class UserAccountModel(BaseModel):
    account_type: str
    account_name: str
    opening_balance: float
    receivable: bool
    payable: bool


class BudgetModel(BaseModel):
    amount: float
    category: str


class SavingGoalsModel(BaseModel):
    saving_amount: float
    reason: str
    targeted_date: str
    category: str


class SavingTransactionModel(BaseModel):
    amount: float
    date: str
    source_account: str
    saving_goal: str


class TransactionModel(BaseModel):
    amount: float
    transaction_type: str
    category: str
    account: str
    date: str
    location: str
    description: str
    recurring_transaction: bool
    interval: str
    recurring_date: str
    recurring_time: str


class TransferTransactionModel(BaseModel):
    amount: float
    transfer_type: str
    account_from: str
    account_to: str
    date: str
    description: str
    location: str
    recurring_transaction: bool
    interval: str
    recurring_date: str
    recurring_time: str


class UpdateTransactionModel(BaseModel):
    transaction_id : str


class UserSettingModel(BaseModel):
    currency: str
    country: str
    amount_format: int
