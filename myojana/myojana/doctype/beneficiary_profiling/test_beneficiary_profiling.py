# Copyright (c) 2023, suvaidyam and Contributors
# See license.txt

import frappe
from frappe import _
import random
import string
from frappe.utils import today, add_days
from frappe.tests.utils import FrappeTestCase


class TestBeneficiaryProfiling(FrappeTestCase):
    def get_random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def get_random_date(self):
        return add_days(today(), -random.randint(365 * 18, 365 * 60))  # 18–60 years old

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_beneficiary_creation_for_mandatory_fields(self):
        meta = frappe.get_meta("Beneficiary Profiling")
        mandatory_fields = [
            {"fieldname": field.fieldname, "fieldtype": field.fieldtype}
            for field in meta.fields if field.reqd
        ]

        doc_data = {"doctype": "Beneficiary Profiling"}
        for field in mandatory_fields:
            fieldname = field["fieldname"]
            fieldtype = field["fieldtype"]

            if fieldname in doc_data:  # skip if already set
                continue

            if fieldtype == "Data":
                doc_data[fieldname] = self.get_random_string()
            elif fieldtype == "Date":
                doc_data[fieldname] = self.get_random_date()
            elif fieldtype == "Int":
                doc_data[fieldname] = random.randint(1, 100)
            elif fieldtype == "Float":
                doc_data[fieldname] = round(random.uniform(1, 100), 2)
            elif fieldtype == "Select":
                field_meta = next((f for f in meta.fields if f.fieldname == fieldname), None)
                if field_meta and field_meta.options:
                    options = field_meta.options.split("\n")
                    doc_data[fieldname] = random.choice(options)
                else:
                    doc_data[fieldname] = ""
            elif fieldtype == "Check":
                doc_data[fieldname] = random.choice([0, 1])
            elif fieldtype == "Link":
                field_meta = next((f for f in meta.fields if f.fieldname == fieldname), None)
                if field_meta and field_meta.options:
                    linked_doctype = field_meta.options
                    linked_docs = frappe.get_all(linked_doctype, limit=10, pluck="name")
                    if linked_docs:
                        doc_data[fieldname] = random.choice(linked_docs)
                    # else:
                    #     # Create dummy entry if none exist

        data = frappe.get_doc(doc_data)
        data.insert(ignore_permissions=True)
        if frappe.get_site_config().get("save_test_records"):
            frappe.db.commit()
        self.assertIsNotNone(data.name, "Document was not assigned a name after insert.")
        fetched = frappe.get_doc("Beneficiary Profiling", data.name)
        self.assertEqual(fetched.name, data.name, "Document could not be retrieved after creation.")
        print(f"✅ Test Beneficiary Profiling passed for: {data.name}")
