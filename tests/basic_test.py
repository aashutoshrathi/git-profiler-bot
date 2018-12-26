from datetime import datetime, timedelta
import pytest
import os
import requests
from handler import stalk
import sys
sys.path.append('../')

# Yeah Testing is cool and totally worth it!
user = 'aashutoshrathi'
delimiter = '</b>'
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


def get_contri_data():
    contri_api = requests.get(
        '{0}{1}/count'.format(os.environ['CONTRI_API'], user))
    contri_data = contri_api.json()
    return contri_data


@pytest.mark.parametrize("actual_key, expected_key", [
    ('Login', 'login'),
    ('Name', 'name'),
    ('Company', 'company'),
    ('Blog', 'blog'),
    ('Public Repos', 'public_repos'),
    ('Public Gists', 'public_gists'),
    ('Followers', 'followers'),
    ('Following', 'following')
])
def test_profile_details(actual_key, expected_key):
    assert str(util(actual_key)) == str(result[expected_key])


def test_contribution_count():
    if result['type'] == 'User':
        now = datetime.now()
        contri_data = get_contri_data()
        y, m, d = "{0}".format(now.year), "{0}".format(
            now.month), "{0}".format(now.day)
        assert str(util("Today\'s Contribution")) == str(
            contri_data.get('data').get(y).get(m).get(d))


def test_streak_count():
    if result['type'] == 'User':
        streak_count = 0
        contri_data = get_contri_data()
        d = datetime.today()
        y, m, d = "{0}".format(d.year), "{0}".format(
            d.month), "{0}".format(d.day)
        while contri_data.get('data').get(y).get(m).get(d) != 0:
            streak_count += 1
            d = datetime.today() - timedelta(days=streak_count)
            y, m, d = "{0}".format(d.year), "{0}".format(
                d.month), "{0}".format(d.day)
        assert str(util('Current Streak')) == str(streak_count) + ' days'
