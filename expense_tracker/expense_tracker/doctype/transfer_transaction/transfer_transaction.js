// Copyright (c) 2024, Manav Mandli and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transfer Transaction", {
  user(frm) {
    frm.set_query("account_from", function () {
      return {
        filters: {
          user: frm.doc.user,
        },
      };
    });
    frm.set_query("account_to", function () {
      return {
        filters: {
          user: frm.doc.user,
        },
      };
    });
  },
});
