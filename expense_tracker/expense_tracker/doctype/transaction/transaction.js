// Copyright (c) 2024, Manav Mandli and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction", {
  transaction_type(frm) {
    frm.set_query("category", function () {
      return {
        filters: {
          catgory_type: frm.doc.transaction_type,
        },
      };
    });
  },
  user(frm) {
    frm.set_query("account", function () {
      return {
        filters: {
          user: frm.doc.user,
        },
      };
    });
  },
});
