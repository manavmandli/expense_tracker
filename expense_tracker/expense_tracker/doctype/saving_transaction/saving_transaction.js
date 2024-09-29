// Copyright (c) 2024, Manav Mandli and contributors
// For license information, please see license.txt

frappe.ui.form.on("Saving Transaction", {
  user(frm) {
    frm.set_query("source_account", function () {
      return {
        filters: {
          user: frm.doc.user,
        },
      };
    });
    frm.set_query("saving_goal", function () {
      return {
        filters: {
          user: frm.doc.user,
        },
      };
    });
  },
});
