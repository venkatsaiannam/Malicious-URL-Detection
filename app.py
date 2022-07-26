from flask import Flask, render_template, request
import pickle
import pandas as pd
from urllib.parse import urlparse
import sklearn
import numpy as np
import re

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/url')
def url():
    model = pickle.load(open("model.pkl", "rb"))

    def having_ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            # IPv6 in hexadecimal
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            # if IP is present
            return 1
        else:
            return 0

    def Numbers_count(url):
        numbers = 0
        for i in url:
            if i.isnumeric():
                numbers = numbers + 1
        return numbers

    def Numbers_ratio(url):
        return Numbers_count(url)/len(url)

    def Alphabets_count(url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters

    def Alphabet_ratio(url):
        return Alphabets_count(url)/len(url)

    def lower(url):
        letters = 0
        for i in url:
            if i.islower():
                letters = letters + 1
        return letters

    def lower_ratio(url):
        return lower(url)/len(url)

    def upper(url):
        letters = 0
        for i in url:
            if i.isupper():
                letters = letters + 1
        return letters

    def special(string):
        count = 0
        for i in range(len(string)):
            if(string[i].isalpha()):
                pass
            elif(string[i].isdigit()):
                pass
            else:
                count = count + 1
        return count

    def special_ratio(string):
        return special(string)/len(string)
    Testing = {}
    url = request.args['url']
    Testing['IP_in_URL'] = having_ip_address(url)
    Testing['URL_len'] = len(str(url))
    Testing['Domain_len'] = len(urlparse(url).netloc)
    Testing['Dots'] = urlparse(url).netloc.count('.')
    Testing['Hyphens'] = urlparse(url).netloc.count('-')
    Testing['Double-slashes'] = url.count('//')
    Testing['At(@)'] = url.count('@')
    Testing['Semicolon(;)'] = url.count(';')
    Testing['And(&)'] = url.count('&')
    Testing['Http'] = url.count('http')
    Testing['Https'] = url.count('https')
    Testing['Numbers'] = Numbers_count(url)
    Testing['Numbers _ratio'] = Numbers_ratio(url)*100
    Testing['Alphabets'] = Alphabets_count(url)
    Testing['Alphabet_ratio'] = Alphabet_ratio(url)*100
    Testing['Lower_case_letters'] = lower(url)
    Testing['Lower_case_letters_ratio'] = lower_ratio(url)*100
    Testing['Upper_case_letters'] = upper(url)
    Testing['Special_char_ratio'] = special_ratio(url)*100

    # Converting Dictionary to DataFrame
    df = pd.DataFrame(Testing, index=[0])

    # Real Time Prediction
    preds = model.predict(df)

    # preds is a numpy datatype that why we are coverting into a integer datatype
    np_int = preds[0]

    py_int = np_int.item()

    if(py_int):
        return render_template('output.html', output="Malicious", color="red")
    else:
        return render_template('output.html', output="Benign", color="green")


if __name__ == "__main__":
    app.run()
