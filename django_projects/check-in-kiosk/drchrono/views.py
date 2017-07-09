from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from forms import *
from api_methods import *
from models import *
from modelForms import *
import datetime, pytz, iso8601

####################################################################################################
################################ Authentication and setup methods ##################################
####################################################################################################

"""
Authentication view that fetches token object for using drchrono APIs and
sets up a list of all the patients with an appointment on the present day
in the database
"""

def auth(request):
    response = get_token(request)
    response.raise_for_status()
    data = response.json()
    # Save these in your database associated with the user
    token = Token.objects.create(
        access_token = data['access_token'],
        refresh_token = data['refresh_token'],
        expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
    )
    token.save()
    # Create an appointment list for the day and redirect to welcome page
    appointments = Appointment.objects.all()
    if appointments != None:
        appointments.delete()
    create_appointment_list(token)
    return redirect("/options")


"""
Creates a complete list of all the patients
with an appointment today and stores that list
in the database in the Appointment object tabel
"""
def create_appointment_list(token):
    appointments, patients = get_patient_appointments(token)
    for a in appointments:
        first_name, last_name, ssn = patients[a['patient']]
        time = iso8601.parse_date(a['scheduled_time'])
        new_appointment = Appointment(pid = a['patient'], first_name = first_name, last_name = last_name, SSN = ssn.replace('-',''), time = time, check_in_time = time, duration = a['duration'])
        new_appointment.save()
    return


####################################################################################################
####################### Options, Status, Welcome, Error and Success Methods ########################
####################################################################################################

"""
Options Page
"""
def options(request):
    return render(request, 'options.html')

"""
Status Page
"""
def status(request):
    appointments = Appointment.objects.all()
    wait_times = ['0m 0s'] * len(appointments)
    return render(request, 'status.html',{'appointments': zip(appointments, wait_times)})

"""
Welcome Page
"""
def welcome(request):
    return render(request, 'welcome.html')


"""
Error Page
"""
def error(request):
    return render(request, 'error.html')


"""
Success Page
"""
def success(request):
    return render(request, 'success.html')



####################################################################################################
############################## View methods used by the status page ################################
####################################################################################################

"""
Used by status page in an ajax call to update
patient's appointment status to 'In Session'
"""
def start_appointment(request):
    pid = request.GET.get('pid')
    appointments = Appointment.objects.filter(pid=pid)
    if appointments:
        for a in appointments:
            if a.status == 'AR':
                a.status = 'INS'
                a.wait_time = find_wait_time(a.check_in_time)
                a.save()
                break
        return HttpResponse('Patient status changed!')
    return HttpResponse('Looks like the patient is done!')


"""
Used by status page in an ajax call to update
patient's appointment status to 'Complete'
"""
def end_appointment(request):
    pid = request.GET.get('pid')
    appointments = Appointment.objects.filter(pid=pid)
    if appointments:
        for a in appointments:
            if a.status == 'INS':
                a.status = 'COM'
                a.save()
                break
        return HttpResponse('Patient removed from list!')
    return HttpResponse('Looks like the patient is done!')


"""
Used by status page in an ajax call to update
patient's waiting time since his/her checking in
"""
def update(request):
    appointments, wait_times = Appointment.objects.all(), []
    for a in appointments:
        if a.check_in_time != a.time:
            wait_times.append(find_wait_time(a.check_in_time))
        else:
            wait_times.append("0m 0s")
    return render(request, 'update.html', {'appointments': zip(appointments, wait_times)})

"""
Helper method to find wait time of a patient
"""
def find_wait_time(check_in_time):
    diff = datetime.datetime.now(pytz.UTC) - check_in_time
    diff =  divmod(diff.days * 86400 + diff.seconds, 60)
    minutes, seconds = diff[0], diff[1]
    return "".join([str(minutes), 'm ', str(seconds), 's'])

####################################################################################################
############################## View methods used in check-in flow ##################################
####################################################################################################

"""
View method used to validate a patient's appointment and
send him further in the check-in process
"""
def check_in(request):
    if request.method == 'POST':
        ssn = request.POST.get('SSN')
        appointments = Appointment.objects.filter(SSN = ssn)
        if appointments:
            for a in appointments:
                if a.checked_in == False:
                    return redirect("/demographics/" + str(a.pid))
        else:
            #redirect to another page showing an error message
            return redirect("/error")
    else:
        form = AppointmentForm()
        return render(request, 'check_in.html', {'form': form})


"""
View method used to render the DemographicInfoForm
for the logged-in patient.
"""
def demographics(request, pid):
    if request.method == 'GET':
        token = Token.objects.get(pk = 1)
        info = get_demographics(token, pid)
        form = DemographicInfoForm({
                                    'email' : info['email'],
                                    'address' : info['address'],
                                    'cell_phone' : info['cell_phone'],
                                    'gender' : info['gender'],
                                    'ethnicity' : info['ethnicity']
                                  })
        return render(request, 'demographics.html', {'form':form, 'pid': pid})


"""
View method used to update a patient's demographic info
and let him complete the check-in process
"""
def update_info(request, pid):
    form = DemographicInfoForm(request.POST)
    if form.is_valid():
        token = Token.objects.get(pk = 1)
        update_demographics(token, form.cleaned_data, pid)
        appointments = Appointment.objects.filter(pid=pid)
        if appointments:
            for a in appointments:
                if a.checked_in == False:
                    a.status = 'AR'
                    a.check_in_time = datetime.datetime.now(pytz.UTC)
                    a.checked_in = True
                    a.save()
                    break
            return redirect("/success")
    else:
        return redirect("/error")   #make this page
