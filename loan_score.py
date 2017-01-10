import json
import io
import re
import random_forest_classifier as rfc
import numpy as np
from urllib2 import URLError
from collections import OrderedDict
from yelp.client import Client
from yelp.errors import BusinessUnavailable
from yelp.oauth1_authenticator import Oauth1Authenticator
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


class Business(object):
    def __init__(self, data):
        self.data = data
        self.rating = {"score": 0, "votes": 0}
        self._yelp_fetch()

    def __str__(self):
        b = []
        for k, v in self.data.iteritems():
            b.append("{}: {}".format(k, v))

        return "\n".join(b)

    def _yelp_fetch(self):
        print "Yelp API Fetch"
        with io.open("config_secret.json") as cred:
            creds = json.load(cred)

        auth = Oauth1Authenticator(**creds["yelp"])
        client = Client(auth)
        params = {"lang": "en"}

        # Format Yelp Business name to word1-word2-... format
        lower_name = re.sub(
            r'([^\s\w]|_)+', '',
            self.data["Business Name"].lower()).split(" ")

        businessName = "-".join(lower_name)
        business = None
        found = False

        try:
            print "Getting business {}".format(businessName)
            business = client.get_business(businessName)
            found = True
        except BusinessUnavailable:
            print "Failed - Trying phone number"
        except URLError:
            print "Could not connect to Yelp"

        if not found:
            try:
                params = {"cc": "US"}
                num = re.sub(r"[^\d]+", "", self.data["Phone Number"])
                response = client.phone_search(num, **params)

                if response.businesses:
                    business = response.businesses[0]
                found = True
            except:
                print "Could not find business on Yelp"

        if found and business is not None:
            self.rating["score"] += business.rating * business.review_count
            self.rating["votes"] += business.review_count
            print "Found Business with rating {}".format(self.rating)


def parse_data(data):
    errors = []

    fields = ["Business Name", "Business Owners", "Phone Number"] + \
        rfc.features

    for f in fields:
        if not data.get(f):
            errors.append("{} not found".format(f))

    if errors:
        raise Exception("\n".join(errors))


def find_score(business):
    score = 0.0
    badRating = (business.rating['votes'] and
                 business.rating['score'] / business.rating['votes'] <= 2.5)

    if (badRating or
       business.data["Loan Amount"] >= business.data["Annual Income"]):
        print "P-Score is 0"
        return score

    loan_model = joblib.load('random_forest.pkl')

    data = []
    for k, v in business.data.iteritems():
        if k in rfc.features:
            try:
                data.append(float(v))
            except ValueError:
                raise Exception("Expected number, found {}".format(v))

    score = loan_model.predict_proba(data)
    print "P-Score is {}".format(score[0][0])
    return score

if __name__ == "__main__":
    # Accepts JSON string
    with open("data.json") as f:
        try:
            data = json.load(f, object_pairs_hook=OrderedDict)
            success = True
        except:
            print "JSON not formatted correctly"
            success = False
    if success:
        parse_data(data)
        business = Business(data)
        score = find_score(business)
