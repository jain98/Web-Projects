from django.conf import settings
from django.utils import timezone
from collections import defaultdict
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
'    Method to retrieve appointments list for the current doctor   '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@isvalid_token
def get_patient_appointments(token):
    headers = {'Authorization': 'Bearer %s' % token.access_token}
    filters = {'date': "2016-12-12"}    #str(datetime.date.today())
    appointments_url = 'https://drchrono.com/api/appointments'
    data = requests.get(appointments_url, headers=headers, params=filters).json()
    appointments = data['results']
    patient_ids = [appointments[i]['patient'] for i in range(len(appointments))]
    patients = get_patients_with_appointments(token, patient_ids)
    return appointments, patients


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'       Method to retrieve patients with appointments today        '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@isvalid_token
def get_patients_with_appointments(token, patient_ids):
    headers = {'Authorization': 'Bearer %s' % token.access_token}
    patients, patients_url, i = defaultdict(list), 'https://drchrono.com/api/patients', 0
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        for i in range(len(data['results'])):
            if data['results'][i]['id'] in patient_ids:
                info = [data['results'][i]['first_name'], data['results'][i]['last_name'], data['results'][i]['social_security_number']]
                patients[data['results'][i]['id']] = info
        patients_url = data['next'] # A JSON null on the last page
    return patients



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'         Method to retrieve demographic info of a patient         '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@isvalid_token
def get_demographics(token, pid):
    headers = {'Authorization': 'Bearer %s' % token.access_token}
    url = 'https://drchrono.com/api/patients/' + pid
    data = requests.get(url, headers=headers).json()
    return data


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'         Method to update demographic info of a patient         '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@isvalid_token
def update_demographics(token, form, pid):
    form['doctor'] = 100726
    headers = {'Authorization': 'Bearer %s' % token.access_token}
    url = 'https://drchrono.com/api/patients/' + pid
    data = requests.put(url, data=form, headers=headers)
    return data
