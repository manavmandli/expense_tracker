import frappe


# def get_items():
#     frappe.response["message"] = "Item list get successfully"
#     return frappe.db.sql(
#         """
#         SELECT
#             item.*,
#             item_price.price_list_rate
#         FROM
#             `tabItem` AS item
#         LEFT JOIN
#             `tabItem Price` AS item_price ON item.name = item_price.item_code
#         """,
#         as_dict=True,
#     )


# def get_category():
#     frappe.response["message"] = "Item Group list get successfully"
#     return frappe.get_all("Item Group", filters={"is_group": 0}, fields=["name"])
