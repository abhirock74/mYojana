import frappe
import datetime
import random
import string
import uuid


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


def calculate_age(date_of_birth):
    dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
    current_date = datetime.datetime.now()

    age = current_date.year - dob.year
    month_diff = current_date.month - dob.month

    if month_diff < 0 or (month_diff == 0 and current_date.day < dob.day):
        age -= 1
        month_diff += 12

    return age, month_diff


@frappe.whitelist()
def create_beneficiary_profiling():
    # Fetching required master data
    Caste_category = frappe.get_list('Caste category', pluck='name')
    Schemes = frappe.get_list('Scheme', pluck='name')
    Religion = frappe.get_list('Religion', pluck='name')
    Education = frappe.get_list('Education', pluck='name')
    Occupation = frappe.get_list('Occupation', pluck='name')
    Marital_status = frappe.get_list('Marital status', pluck='name')
    Sub_Centre = frappe.get_list('Sub Centre', pluck='name')
    Source_Of_Information = frappe.get_list(
        'Source Of Information', pluck='name')
    Social_vulnerable_category = frappe.get_list(
        'Social vulnerable category', pluck='name')
    House_Types = frappe.get_list('House Types', pluck='name')
    ID_Document = frappe.get_list('ID Document', pluck='name')
    Proof_of_Disability = frappe.get_list('Proof of Disability', pluck='name')
    Village = frappe.get_list(
        'Village', filters={'state': 'S07'}, pluck='name')

    # Creating 1000 instances of Beneficiary Profiling
    for index in range(10):
        print("???????????????????????????????????????????", index)
        date_of_birth = random_date(datetime.datetime(
            1950, 1, 1), datetime.datetime(2010, 1, 1)).strftime("%Y-%m-%d")
        completed_age, completed_age_month = calculate_age(date_of_birth)

        random_oc = random.choice(Occupation)
        random_occ = frappe.get_value(
            'Occupation', random_oc, 'occupational_category')

        random_sub_center = random.choice(Sub_Centre)
        random_center = frappe.get_value(
            'Sub Centre', random_sub_center, 'centre')

        soi = random.choice(Source_Of_Information)
        ms = random.choice(Marital_status)
        sv = random.choice(["Yes", "No"])
        pwd = random.choice(["Yes", "No"])
        vil = random.choice(Village)
        wards = frappe.get_value('Village', vil, 'block')
        dis = frappe.get_value('Village', vil, 'district')
        any_doc = random.choice(["Yes", "No"])
        weyd = random.choice(["Below 40%", "Above 40%", "Do not know"])
        scheme = random.choice(Schemes)
        Milestone_category = frappe.get_value('Scheme', scheme, 'milestone')
        name_of_department = frappe.get_value(
            'Scheme', scheme, 'name_of_department')
        beneficiary = frappe.new_doc("Beneficiary Profiling")
        beneficiary.update({
            "doctype": "Beneficiary Profiling",
            "date_of_visit": random_date(datetime.datetime(2020, 1, 1), datetime.datetime(2024, 1, 1)).strftime("%Y-%m-%d"),
            "name_of_the_beneficiary": random_string(10),
            "gender": random.choice(["Male", "Female", "Transgender", "Others"]),
            "date_of_birth": date_of_birth,
            "completed_age": completed_age,
            "completed_age_month": completed_age_month,
            "contact_number": ''.join(random.choice(string.digits) for _ in range(10)),
            "alternate_contact_number": ''.join(random.choice(string.digits) for _ in range(10)),
            "centre": random_center,
            "sub_centre": random_sub_center,
            "source_of_information": soi,
            **({"name_of_the_camp": random.choice(frappe.get_list('Camp', pluck='name'))} if soi == 'Camp' else {}),
            "has_anyone_from_your_family_visisted_before": 'No',
            "caste_category": random.choice(Caste_category),
            "religion": random.choice(Religion),
            "education": random.choice(Education),
            "current_occupation": random_oc,
            "occupational_category": random_occ,
            "marital_status": ms,
            **({"spouses_name": random_string(10)} if ms == 'Married' else {}),
            "social_vulnerable": sv,
            **({"social_vulnerable_category": random.choice(Social_vulnerable_category)} if sv == 'Yes' else {}),
            "are_you_a_person_with_disability_pwd": pwd,
            **({"type_of_disability": random.choice([
                "Blindness", "Low vision", "Leprosy cured persons", "Locomotor disability", "Dwarfism",
                "Intellectual disability", "Mental illness", "Cerebral Palsy", "Specific learning disability",
                "Speech and Language disability", "Hearing impairment", "Muscular dystrophy", "Acid attack victim",
                "Parkinson's disease", "Multiple Sclerosis", "Thalassemia", "Hemophilia", "Sickle cell disease",
                "Autism spectrum disorder", "Chronic neurological conditions", "Multiple disabilities including deaf and blindness"
            ])} if pwd == 'Yes' else {}),
            **({"what_is_the_extent_of_your_disability": weyd} if pwd == 'Yes' else {}),
            **({"proof_of_disability": random.choice(Proof_of_Disability)
                } if weyd == 'Above 40%' else {}),
            "annual_income": random.randint(10000, 1000000),
            "do_you_have_any_bank_account": random.choice(["Yes", "No"]),
            "fathers_name": random_string(10),
            "mothers_name": random_string(10),
            "added_by": 'Administrator',
            "current_house_type": random.choice(House_Types),
            "state": 'S07',
            "state_of_origin": 'S07',
            "district": dis,
            "ward": wards,
            "name_of_the_settlement": vil,
            "do_you_have_any_id_documents": any_doc
        })

        if any_doc == 'Yes':
            for i in range(3):
                beneficiary.append("id_table_list", {
                    "doctype": "ID Document Child",
                    "enter_id_number": ''.join(random.choice(string.digits) for _ in range(12)),
                    "which_of_the_following_id_documents_do_you_have": random.choice(ID_Document)
                })

        for i in range(5):
            beneficiary.append("scheme_table", {
                "amount_paid": random.randint(500, 1000),
                "application_number": f"APP-{uuid.uuid4().hex[:6]}",
                "application_submitted": random.choice(["No", "Yes", "Completed", "Previously availed"]),
                "date_of_application": datetime.datetime.now().strftime("%Y-%m-%d"),
                "milestone_category": Milestone_category,
                "mode_of_application": random.choice(["Online", "Offline"]),
                "name_of_the_department": name_of_department,
                "name_of_the_scheme":  scheme[0],
                "paid_by": random.choice(["Self", "CSC"]),
                "reason_of_application": "any",
                "remarks": "any"
            })

            beneficiary.append("follow_up_table", {
                "follow": random_sub_center,
                "follow_up_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "follow_up_mode": random.choice(["Home visit", "Phone call", "Centre visit", "In-person visit"]),
                "follow_up_status": random.choice(["Interested", "Not interested", "Document submitted", "Under process", "Completed", "Rejected", "Additional info required"]),
                "follow_up_with": random.choice(["Beneficiary", "Government department", "Government website", "Others"]),
                "name_of_the_scheme": scheme[0],
                "remarks": "any"
            })
            result = beneficiary.save()
            return result
