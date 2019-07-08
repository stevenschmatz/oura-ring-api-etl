"""
extract.py
"""

import datetime
import os

import mechanize
import rauth
import requests


USER_EMAIL = os.environ.get('USER_EMAIL')
USER_PASSWORD = os.environ.get('USER_PASSWORD')

OURA_CLIENT_ID = os.environ.get('OURA_CLIENT_ID')
OURA_CLIENT_SECRET = os.environ.get('OURA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

OURA_AUTHORIZE_URL = 'https://cloud.ouraring.com/oauth/authorize'
OURA_ACCESS_TOKEN_URL = 'https://api.ouraring.com/oauth/token'
OURA_BASE_URL = 'https://api.ouraring.com'


def get_oauth2_token(email='', password=''):
    """Get the OAuth2 token by simulating a browser session."""
    # get the authorization URL
    oura = rauth.OAuth2Service(
        client_id=OURA_CLIENT_ID,
        client_secret=OURA_CLIENT_SECRET,
        name='oura',
        authorize_url=OURA_AUTHORIZE_URL,
        access_token_url=OURA_ACCESS_TOKEN_URL,
        base_url=OURA_BASE_URL)

    url = oura.get_authorize_url(
        scope='email personal daily',
        response_type='code',
        redirect_uri=REDIRECT_URI)

    # simulate a browser session to automate email + password entry
    br = mechanize.Browser()
    br.set_handle_equiv(False)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.open(url)
    br.select_form(nr=0)

    # fill in email and password to first form
    br.form['email'] = email
    br.form['password'] = password
    br.submit()

    # set full permissions on second form and retrieve the authorization code
    br.select_form(nr=0)
    br.find_control(name="scope_personal").items[0].selected = True
    br.find_control(name="scope_daily").items[0].selected = True
    br.submit(name="allow")
    url = br.geturl()
    code = url[url.index('?code=') + 6:]

    # retrieve the access token
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    auth = requests.auth.HTTPBasicAuth(OURA_CLIENT_ID, OURA_CLIENT_SECRET)
    resp = requests.post(OURA_ACCESS_TOKEN_URL, data=data, auth=auth).json()

    return resp['access_token']


def get_yesterday_datestamp():
    """Return the ISO date of yesterday."""
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(days = 1)
    return yesterday.isoformat()


def load_daily_data(date=get_yesterday_datestamp()):
    """Scrape all daily stats for sleep, activity, readiness."""
    token = get_oauth2_token(email=USER_EMAIL, password=USER_PASSWORD)

    def get(endpoint):
        """A wrapper around GET requests to the API."""
        headers = {'Authorization': f'Bearer {token}'}

        url = OURA_BASE_URL
        url += endpoint
        url += f'?start={date}&end={date}'

        return requests.get(url, headers=headers).json()

    return {
        'sleep': get('/v1/sleep')['sleep'],
        'activity': get('/v1/activity')['activity'],
        'readiness': get('/v1/readiness')['readiness']
    }