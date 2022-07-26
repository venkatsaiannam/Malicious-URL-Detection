import math
import pandas as pd
from urllib.parse import urlparse
import re
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import warnings
import pickle
from sklearn import metrics
warnings.filterwarnings("ignore")


url_data = pd.read_csv("Dataset.csv")
url_data = url_data.drop('sno', axis=1)


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


url_data['IP_in_URL'] = url_data['url'].apply(lambda i: having_ip_address(i))
url_data['URL_len'] = url_data['url'].apply(lambda i: len(str(i)))
url_data['Domain_len'] = url_data['url'].apply(
    lambda i: len(urlparse(i).netloc))
url_data['Dots'] = url_data['url'].apply(
    lambda i: (urlparse(i).netloc.count('.')))
url_data['Hyphens'] = url_data['url'].apply(
    lambda i: (urlparse(i).netloc.count('-')))
url_data['Underscores'] = url_data['url'].apply(
    lambda i: (urlparse(i).netloc.count('_')))
url_data['Double-slashes'] = url_data['url'].apply(lambda i: i.count('//'))
url_data['At(@)'] = url_data['url'].apply(lambda i: i.count('@'))
url_data['Hash(#)'] = url_data['url'].apply(lambda i: i.count('#'))
url_data['Semicolon(;)'] = url_data['url'].apply(lambda i: i.count(';'))
url_data['And(&)'] = url_data['url'].apply(lambda i: i.count('&'))
url_data['Http'] = url_data['url'].apply(lambda i: i.count('http'))
url_data['Https'] = url_data['url'].apply(lambda i: i.count('https'))


def Numbers_count(url):
    numbers = 0
    for i in url:
        if i.isnumeric():
            numbers = numbers + 1
    return numbers


url_data['Numbers'] = url_data['url'].apply(lambda i: Numbers_count(i))


def Numbers_ratio(url):
    return Numbers_count(url)/len(url)


url_data['Numbers _ratio'] = url_data['url'].apply(
    lambda i: Numbers_ratio(i)*100)


def Alphabets_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


url_data['Alphabets'] = url_data['url'].apply(lambda i: Alphabets_count(i))


def Alphabet_ratio(url):
    return Alphabets_count(url)/len(url)


url_data['Alphabet_ratio'] = url_data['url'].apply(
    lambda i: Alphabet_ratio(i)*100)

# Counting the lowercase characters in the URL and their Ratios


def lower(url):
    letters = 0
    for i in url:
        if i.islower():
            letters = letters + 1
    return letters


url_data['Lower_case_letters'] = url_data['url'].apply(lambda i: lower(i))


def lower_ratio(url):
    return lower(url)/len(url)


url_data['Lower_case_letters_ratio'] = url_data['url'].apply(
    lambda i: lower_ratio(i)*100)

# Counting the uppercase characters in the URL and their Ratios


def upper(url):
    letters = 0
    for i in url:
        if i.isupper():
            letters = letters + 1
    return letters


url_data['Upper_case_letters'] = url_data['url'].apply(lambda i: upper(i))


def upper_ratio(url):
    return upper(url)/len(url)


url_data['Upper_case_letters_ratio'] = url_data['url'].apply(
    lambda i: upper_ratio(i)*100)

# Counting the special characters in the URL and their Ratios


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


url_data['Special_char'] = url_data['url'].apply(lambda i: special(i))


def special_ratio(string):
    return special(string)/len(string)


url_data['Special_char_ratio'] = url_data['url'].apply(
    lambda i: special_ratio(i)*100)


url_data = url_data.drop('Underscores', axis=1)
url_data = url_data.drop('Hash(#)', axis=1)
url_data = url_data.drop('Upper_case_letters_ratio', axis=1)
url_data = url_data.drop('Special_char', axis=1)

url_data.to_csv("dataset_reduce.csv")

x = url_data[['IP_in_URL', 'URL_len', 'Domain_len', 'Dots', 'Hyphens', 'Double-slashes', 'At(@)', 'Semicolon(;)',
              'And(&)', 'Http', 'Https', 'Numbers', 'Numbers _ratio', 'Alphabets', 'Alphabet_ratio', 'Lower_case_letters', 'Lower_case_letters_ratio',
              'Upper_case_letters', 'Special_char_ratio']]

# Target Variable
y = url_data[['result']]


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=123)

sn = SMOTE(random_state=123)
x_train_res, y_train_res = sn.fit_resample(x_train, y_train)
Y = y_train_res['result']
x_train, x_test, y_train, y_test = train_test_split(
    x_train_res, Y, train_size=0.7, random_state=42)


rfc = RandomForestClassifier()

model_rfc = rfc.fit(x_train, y_train)

y_pred = model_rfc.predict(x_test)

pickle.dump(model_rfc, open("model.pkl", "wb"))
model = pickle.load(open("model.pkl", "rb"))
