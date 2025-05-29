# Copyright (c) 2023, suvaidyam and Contributors
# See license.txt

import frappe
from frappe import _
from frappe.utils import today
import random
import string
from frappe.tests.utils import FrappeTestCase
from sva_unittest.tests.utils import create_random_doc , get_random_mobile_number , generate_random_indian_name
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

class TestBeneficiaryProfiling(FrappeTestCase):
    def setUp(self):
        print(f"{BLUE}🔍 Starting setup for TestBeneficiaryProfiling...{RESET}")

    def test_beneficiary_creation_for_mandatory_fields(self):
        print(f"{YELLOW}🔍🔍 Starting test: Creating Beneficiary Profiling with mandatory fields...{RESET}")
        ben_doc = create_random_doc(
            "Beneficiary Profiling",
            only_mandatory=True,
            what_is_the_extent_of_your_disability="Below 40%",
            contact_number = get_random_mobile_number(),
            date_of_visit= today(),
            name_of_the_beneficiary = generate_random_indian_name(),
            is_bulk_imported=False,
        )
        print(f"{GREEN}✅ Document created, checking if 'name' is assigned...{RESET}")
        self.assertIsNotNone(ben_doc.name, "Failed to create Beneficiary Profiling with mandatory fields.")

        print(f"{YELLOW}🔍 Fetching document '{ben_doc.name}' from DB...{RESET}")
        fetched = frappe.get_doc("Beneficiary Profiling", ben_doc.name)
        
        print(f"{GREEN}✅ Document fetched, verifying its name...{RESET}")
        self.assertEqual(fetched.name, ben_doc.name, "Document could not be retrieved after creation.")
        print(f"{GREEN}🎉 Test passed: Successfully created and verified 'Beneficiary Profiling' document with name '{ben_doc.name}'.{RESET}")

    def test_beneficiary_creation_for_all_fields(self):
        print(f"{YELLOW}🔍🔍 Starting test: Creating Beneficiary Profiling with all fields...{RESET}")
        ben_doc = create_random_doc(
            "Beneficiary Profiling",
            only_mandatory=False,
            name_of_the_beneficiary = generate_random_indian_name(),
            what_is_the_extent_of_your_disability="Below 40%",
            contact_number = get_random_mobile_number(),
            alternate_contact_number = get_random_mobile_number(),
            date_of_visit=today(),
            is_bulk_imported=False,
        )
        print(f"{GREEN}✅ Document created, checking if 'name' is assigned...{RESET}")
        self.assertIsNotNone(ben_doc.name, "Failed to create Beneficiary Profiling with all fields.")

        print(f"{YELLOW}🔍 Fetching document '{ben_doc.name}' from DB...{RESET}")
        fetched = frappe.get_doc("Beneficiary Profiling", ben_doc.name)
        
        print(f"{GREEN}✅ Document fetched, verifying its name...{RESET}")
        self.assertEqual(fetched.name, ben_doc.name, "Document could not be retrieved after creation.")
        print(f"{GREEN}🎉 Test passed: Successfully created and verified 'Beneficiary Profiling' document with name '{ben_doc.name}'.{RESET}")

    def test_beneficiary_creation_with_invalid_data(self):
        print(f"{YELLOW}🔍🔍 Starting test: Creating Beneficiary Profiling with invalid data...{RESET}")
        with self.assertRaises(frappe.ValidationError):
            ben_doc = create_random_doc(
                "Beneficiary Profiling",
                only_mandatory=False,
                what_is_the_extent_of_your_disability="Invalid Data",  # Invalid data
                date_of_visit=today(),
                is_bulk_imported=False,
            )
        print(f"{RED}❌ Test passed: Caught expected ValidationError for invalid data.{RESET}")
        

    def tearDown(self):
        pass
