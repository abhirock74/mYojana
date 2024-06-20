// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
var filters = [
	{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "From Date",
	},
	{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": "To Date"
	},
];
frappe.query_reports["Beneficiaries who have received benefits of at least 1 scheme in each category"] = {
	filters: filters
};
