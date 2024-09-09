// Copyright (c) 2024, Manav Mandli and contributors
// For license information, please see license.txt

frappe.ui.form.on("User Account", {
  refresh(frm) {
    frm.set_value("user", frappe.session.user);
  },
  payable: function (frm) {
    if (frm.doc.payable) {
      frm.set_value("receivable", 0);
    }
  },
  receivable: function (frm) {
    if (frm.doc.receivable) {
      frm.set_value("payable", 0);
    }
  },
});
