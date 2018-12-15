import sys
sys.path.append('../')
from handler import stalk
import requests
import os
import datetime

# Yeah Testing is cool and totally worth it!
user = 'aashutoshrathi'
delimiter = '</strong>'
os.environ['CONTRI_API'] = 'https://github-contributions-api.herokuapp.com/'

profile = stalk(user)
profile_details = profile.split('\n')

api = requests.get("https://api.github.com/users/" + user)
result = api.json()

def util(key):
    value = ''
    for detail in profile_details:
        if key in detail:
            starting_index = detail.find(delimiter) + len(delimiter) + 1
            value = detail[starting_index:]
    return value

def test_username():
    assert util('Login') == str(result['login'])

def test_user_type():
    assert util('Type') == str(result['type'])

def test_name():
    assert util('Name') == str(result['name'])

def test_company():
    assert util('Company') == str(result['company'])

def test_blog():
    assert util('Blog') == str(result['blog'])

def test_email():
    assert util('Email') == str(result['email'])

def test_public_repos():
    assert int(util('Public Repos')) == result['public_repos']

def test_public_gists():
    assert int(util('Public Gists')) == result['public_gists']

def test_followers():
    assert int(util('Followers')) == result['followers']

def test_following():
    assert int(util('Following')) == result['following']

def test_contribution_count():
    if result['type'] == 'User':
        now = datetime.datetime.now()
        contri_api = requests.get('{0}{1}/count'.format(os.environ['CONTRI_API'], user))
        contri_data = contri_api.json()
        y, m, d = "{0}".format(now.year), "{0}".format(now.month), "{0}".format(now.day)
        assert str(util("Today\'s Contribution")) == str(contri_data.get('data').get(y).get(m).get(d))
