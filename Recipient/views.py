from django.shortcuts import render, redirect
from .models import recipient
from authentication.models import bloodbank, userprofile
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

# Create your views here. 
def request_blood(request): 
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = recipient(
                recipientname=request.POST.get('recipientname'),
                recipientphone=request.POST.get('recipientphone'),
                recipientlocation=request.POST.get('recipientlocation'),
                recipientage=request.POST.get('recipientage'),
                recipientgender=request.POST.get('recipientgender'),
                recipientblood=request.POST.get('recipientblood'),
                recipientdonationtype=request.POST.get('recipientdonationtype'),
                recipientdonationquantity=request.POST.get('recipientdonationquantity'),
                recipientcondition=request.POST.get('recipientcondition'),
                recipientdate=request.POST.get('recipientdate'),
                recipienttime=request.POST.get('recipienttime'),
            )
            data.save()

            blood_banks = bloodbank.objects.all()
            for bank in blood_banks:
                email_subject = "Donation Request"
                message = render_to_string('donationemail.html', {
                    'recipient_name': data.recipientname,
                    'recipient_phone': data.recipientphone,
                    'recipient_location': data.recipientlocation,
                    'recipient_age': data.recipientage,
                    'recipient_gender': data.recipientgender,
                    'recipient_blood': data.recipientblood,
                    'recipient_donationtype': data.recipientdonationtype,
                    'recipient_donationquantity': data.recipientdonationquantity,
                    'recipient_condition': data.recipientcondition,
                    'recipient_date': data.recipientdate,
                    'recipient_time': data.recipienttime,
                    'bank_name': bank.bloodbankname,
                    'domain': '127.0.0.1:8000',
                })

                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [bank.bloodbankemail]
                )
                email_message.send()

            return redirect("/donor/donation-request/")
        return render(request, "requestblood.html") 
    else:
        messages.warning(request, "PLEASE LOG IN TO REQUEST")
        return redirect('/')

def blood_availability(request): 

    bankdata = bloodbank.objects.all()
    users_with_profiles = User.objects.filter(userprofile__isnull=False).select_related('userprofile')

    if request.method == "GET":
        search_blood_group = request.GET.get('searchBloodGroup', None)
        search_location = request.GET.get('searchAddress', None)
        search_type = request.GET.get('searchType', None)

        donors = []

        for user in users_with_profiles:
            if user.userprofile.phone:
                donors.append(user)

        if search_blood_group or search_location:
            
            if search_blood_group:
                bankdata=bloodbank.objects.filter(bloodbankgroups__icontains = search_blood_group)
                donors = [user for user in donors if user.userprofile.bloodgroup.lower() == search_blood_group.lower()]

            if search_location:
                bankdata=bloodbank.objects.filter(bloodbanklocation__icontains = search_location)
                search_parts = search_location.split()
                for part in search_parts:
                    donors = [user for user in donors if part.lower() in user.userprofile.location.lower()]



        if search_type == 'Donor':
            bankdata = ""
            if search_blood_group:
                donors = [user for user in donors if user.userprofile.bloodgroup.lower() == search_blood_group.lower()]
            if search_location:
                search_parts = search_location.split()
                for part in search_parts:
                    donors = [user for user in donors if part.lower() in user.userprofile.location.lower()]

        if search_type == 'BloodBank':
            donors = ""
            if search_blood_group:
                bankdata=bloodbank.objects.filter(bloodbankgroups__icontains = search_blood_group)
            if search_location:
                bankdata=bloodbank.objects.filter(bloodbanklocation__icontains = search_location)


    data={
        'bankdata' : bankdata,
        'users' : donors,
    }
    return render(request, "bloodavailability.html", data)