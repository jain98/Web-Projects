from django.conf import settings
from django.utils import timezone
import requests, datetime, json, pytz

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'  Decorator for checking if an access toke needs to be refreshed  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def isvalid_token(func):
    def func_wrapper(*args, **kwargs):
        token = args[0]
        if token.expires_timestamp < timezone.now():
            data = refresh_token(token).json()
            token.access_token = data['access_token']
            token.refresh_token = data['refresh_token']
            token.expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
            token.save()
        return func(*args, **kwargs)
    return func_wrapper



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'  Method to refresh expired access_token to use the drchrono api  '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def refresh_token(token):
    response = requests.post('https://drchrono.com/o/token/', data={
    'refresh_token': token.refresh_token,
    'grant_type': 'refresh_token',
    'client_id': settings.SOCIAL_AUTH_DRCHRONO_KEY,
    'client_secret': settings.SOCIAL_AUTH_DRCHRONO_SECRET,
    })
    return response



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Method to retrieve access token in order to use the drchrono api '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def get_token(request):
    '''Method to retrieve access token in order to use the drchrono api'''
    # Check if the provider did not authorize the application to access his/her data
    try:
        error = request.GET['error']
        if error:
            raise ValueError('Error authorizing application: %s' % error)
    except KeyError:
        pass   # Application was properly authorized

    #  Application authorized by provider
    code = request.GET['code']
    response = requests.post('https://drchrono.com/o/token/', data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://127.0.0.1:8000/complete/drchrono/',
        'client_id': settings.SOCIAL_AUTH_DRCHRONO_KEY,
        'client_secret': settings.SOCIAL_AUTH_DRCHRONO_SECRET,
    })
    return response



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'     Method to retrieve patients list for the current doctor      '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Filter method to filter patients by day and month of birthday since
# the api birthdate filtering parameter does not do that inherently

def is_bday_today(today, bday):
    _, m1, d1 = map(int, today.split("-"))
    _, m2, d2 = map(int, bday.split("-"))
    return (today.month == m) and (today.day == d)

@isvalid_token
def get_patients(token):
    headers = {'Authorization': 'Bearer %s' % token.access_token}
    patients, patients_url, i = [], 'https://drchrono.com/api/patients', 0
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        #if is_bday_today(str(datetime.date.today()), data['results'][i]['date_of_birth']):
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page
        i += 1
    return patients[:5]
