Installation

    pip install -r --user requirements.txt


API Keys

    1. Copy config_sample.json into a "config_secret.json" file
    2. Fill in with API Keys
    3. Save "config_secret.json" in same directory as credit_score.py


Usage:
    
    1. Fill data.json with values to be tested
        (Every key is required)

    2. "python loan_score.py"


Tests:

    - "python tests.py"


Description

    Generates a P-Score between 0 - 1 on how likely loan will default.

    Uses a Random Forest model and Yelp statistics to generate P-Score.

    - Trained using loan_data.csv, dataset created from Lending Club public data (2016 Q1 - Q3)
    - Training data contains only small business loans

    Features Used from loan_data.csv:
        Col #    Column
        1 - Loan Amount
        3 - Interest Rate (converted to float)
        4 - Installment
        8 - Employment Length (converted to float)

        10 - Annual Income
        18 - Monthly Debt to Income Ratio
        19 - Delinquencies over 2 Years

        21 - Inquiries in last 6 months
        24 - Open credit lines
        26 - credit revolving balance

        27 - credit utilization rate (converted to float)
        28 - total credit lines

    Classification:
        Not Default - Fully Paid, Grace Period, 15-30 day late

        Default - 30-120 Day Late, Charged Off

Notes:

    - No feature stood out as being highly correlated to P-Score

