import unittest
import random_forest_classifier as rfm
import loan_score as ls


class TestRandomForestClassifier(unittest.TestCase):
    def test_year_to_num_less_than(self):
        self.assertEqual(rfm.yearsToNum("<   osdfi"), 0.5)

    def test_year_to_num_10_plus_years(self):
        self.assertEqual(rfm.yearsToNum("10+ years"), 10.0)

    def test_year_to_num_invalid_num(self):
        self.assertEqual(rfm.yearsToNum("hello"), 0.0)


class TestLoanScore(unittest.TestCase):
    def test_parse_data_all_errors(self):
        data = {}
        errors = ("Business Name not found"
                  "Business Owners not found"
                  "Phone Number not found"
                  "Loan Amount not found"
                  "Interest Rate not found"
                  "Installment not found"
                  "Employment Length not found"
                  "Annual Income not found"
                  "Monthly Debt to Income Ratio not found"
                  "Delinquencies Over 2 Years not found"
                  "Inquiries Last 6 Months not found"
                  "Open Credit Lines not found"
                  "Credit Revolving Balance not found"
                  "Credit Utilization Rate not found"
                  "Total Credit Lines not found")

        with self.assertRaises(Exception) as context:
            ls.parse_data(data)

        self.assertFalse(errors in context.exception)

    def test_parse_data_no_errors(self):
        data = {
            "Business Name": "Luigi's Pizzeria",
            "Business Owners": "Mario, Toad",
            "Phone Number": "516-294-7400",
            "Loan Amount": "10000",
            "Interest Rate": "0.11",
            "Installment": "329.00",
            "Employment Length": "6",
            "Annual Income": "75000",
            "Monthly Debt to Income Ratio": "4.6",
            "Delinquencies Over 2 Years": "0",
            "Inquiries Last 6 Months": "2",
            "Open Credit Lines": "8",
            "Credit Revolving Balance": "5500",
            "Credit Utilization Rate": "0.4",
            "Total Credit Lines": "12"
        }

        self.assertIsNone(ls.parse_data(data))

    def test_bad_yelp_score(self):
        b = ls.Business({
            "Business Name": "test",
            "Phone Number": "111-111-1111"
        })
        b.rating['votes'] = 4
        b.rating['score'] = 4
        self.assertEqual(ls.find_score(b), 0.0)

    def test_loan_amount_too_high(self):
        b = ls.Business({
            "Business Name": "test",
            "Phone Number": "111-111-1111",
            "Loan Amount": "1000000",
            "Annual Income": "10000"
        })
        b.rating['votes'] = 4
        b.rating['score'] = 16
        self.assertEqual(ls.find_score(b), 0.0)

if __name__ == '__main__':
    unittest.main()
