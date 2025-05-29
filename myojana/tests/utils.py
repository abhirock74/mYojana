import frappe
import random
import string
from frappe.utils import today, add_days

def generate_random_indian_name():
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna", "Lakshmi", "Ananya"]
    last_names = ["Sharma", "Patel", "Gupta", "Singh", "Kumar", "Reddy", "Iyer", "Nair", "Choudhury", "Das"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_random_string(length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

def get_random_date():
        return add_days(today(), -random.randint(365 * 18, 365 * 60))

def get_random_mobile_number():
        first_digit = random.choice(['6', '7', '8', '9'])
        remaining_digits = ''.join(random.choices(string.digits, k=9))
        return first_digit + remaining_digits

def get_random_email():
        return f"{get_random_string(8)}@test.com"

def get_random_address():
        return f"{get_random_string(10)}, {get_random_string(5)}, {get_random_string(5)} - {random.randint(100000, 999999)}"

def get_random_pan_number():
        return f"{get_random_string(5).upper()}{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])}{get_random_string(4).upper()}"

def get_random_aadhaar_number():
        return ''.join(random.choices(string.digits, k=12))

def get_random_voter_id():
        return f"{get_random_string(3).upper()}{random.randint(100000, 999999)}"

def get_doctype_fields(doctype, only_mandatory=False):
    meta = frappe.get_meta(doctype)
    if not only_mandatory:
        return [{"fieldname": field.fieldname, "fieldtype": field.fieldtype, "options": field.options} for field in meta.fields]
    else:
        return [
            {"fieldname": field.fieldname, "fieldtype": field.fieldtype, "options": field.options}
            for field in meta.fields if field.reqd
        ]

def get_random_field_value(field):
    fieldtype = field["fieldtype"]
    if fieldtype == "Data":
        return get_random_string(15)
    elif fieldtype == "Date":
        return get_random_date()
    elif fieldtype == "Int":
        return random.randint(1, 100)
    elif fieldtype == "Float":
        return round(random.uniform(1, 100), 2)
    elif fieldtype == "Select":
        options = field.get("options", "").split("\n")
        return random.choice(options) if options else ""
    elif fieldtype == "Check":
        return random.choice([0, 1])
    elif fieldtype == "Link":
        linked_doctype = field.get("options")
        if not linked_doctype:
            return None  # Skip if no linked Doctype is defined
        linked_docs = frappe.get_all(linked_doctype, fields=["name"])
        if linked_docs:
            return random.choice(linked_docs)["name"]
        else:
            linked_new_doc = create_random_doc(linked_doctype, only_mandatory=True)
            if linked_new_doc:
                return linked_new_doc.name
            else:
                return None
    else:
        return None

def create_random_doc(doctype, only_mandatory=False, **kwargs):
    fields = get_doctype_fields(doctype, only_mandatory)
    doc_data = {"doctype": doctype, **kwargs}  # merge kwargs first

    for field in fields:
        fieldname = field["fieldname"]
        if fieldname not in doc_data or doc_data[fieldname] is None:
            doc_data[fieldname] = get_random_field_value(field)

    data = frappe.get_doc(doc_data)
    data.insert(ignore_permissions=True)

    if frappe.conf.get("save_test_records"):
        frappe.db.commit()

    return data
