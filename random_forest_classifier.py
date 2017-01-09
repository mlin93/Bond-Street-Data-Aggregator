import csv
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

classifier = "Default"
features = [
        "Loan Amount", "Interest Rate",
        "Installment", "Employment Length",
        "Annual Income", "Monthly Debt to Income Ratio",
        "Delinquencies Over 2 Years", "Inquiries Last 6 Months",
        "Open Credit Lines", "Credit Revolving Balance",
        "Credit Utilization Rate", "Total Credit Lines"]


def yearsToNum(y):
    y = y[:2].strip()
    if y == "<":
        y = "0.5"

    try:
        return float(y)
    except:
        return 0.0


def random_forest(fileName):
    # Filter Data to Selected Rows
    cols = [classifier] + features
    classifier_dict = {"Y": 1, "N": 0}
    conv = {
        "Default": (lambda x: classifier_dict[x]),
        "Employment Length": yearsToNum
    }

    data = pd.read_csv(fileName, header=0, usecols=cols, converters=conv)

    # Get training data as numpy array
    train_data = data.values

    forest = RandomForestClassifier(n_jobs=2, n_estimators=100)

    # Fit Data
    train_samples = train_data[0::, 1::]
    train_classifiers = train_data[0::, 0]
    forest = forest.fit(train_samples, train_classifiers)

    # Un-comment to display feature importance stats
    """
    for feature, imp in zip(cols[1:], forest.feature_importances_):
        print feature, imp
    """

    # Save model
    joblib.dump(forest, 'random_forest.pkl', compress=True)

if __name__ == '__main__':
    random_forest("loan_data.csv")
