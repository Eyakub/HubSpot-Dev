import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    contacts = "https://api.hubspot.com/contacts/v1/lists/all/contacts/all?hapikey={}".format(settings.APP_API_KEY_TEST)
    
    res = requests.get(contacts)
    print(res)
    try:
        response = requests.get(contacts)
    except:
        print('')

    context = {
        "msg": "Success",
        "data": response.json()
    }
    return JsonResponse(context, status=200)



def individual_data(request):
    email = 'eyakubsorkar@gmail.com'
    contact_data = "https://api.hubspot.com/contacts/v1/contact/email/{}/profile?hapikey={}".format(
        email, settings.APP_API_KEY_TEST
    )
    contact_data_response = requests.get(contact_data)
    contact_data_response = contact_data_response.json()
    favorite_book = contact_data_response
    
    headers = {}
    headers['Content-Type']= 'application/json'
    # return JsonResponse(favorite_book)

    try:
        if request.method == 'POST':
            
            data = json.dumps({
                "properties": [
                    {
                        "property": "favorite_book",
                        "value": request.POST.get('new_val')
                    }
                ]
            })
            print('----------prop update---->', data)
            apiCall = "https://api.hubspot.com/contacts/v1/contact/createOrUpdate/email/{}/?hapikey={}".format(
                email, settings.APP_API_KEY_TEST
            )
            try:
                update_response = requests.post(url=apiCall, headers=headers, data=data)
                print('------->', update_response.__dict__)
            except:
                pass
            return JsonResponse(update_response)
    except:
        pass
    context = {
        'favorite_book': favorite_book['properties']['favorite_book']
    }
    return TemplateResponse(request, 'hub_test/update_info.html', context)


@csrf_exempt
def create_contact(request):
    context = {}

    endpoint = 'https://api.hubapi.com/contacts/v1/contact/?hapikey={}'.format(settings.APP_API_KEY_TEST)
    headers = {}
    headers["Content-Type"]="application/json"
    
    if request.method == 'POST':
        try:
            data = json.dumps({
                'properties': [
                    {
                        "property": "email",
                        "value": request.POST.get('email')
                    },
                    # {
                    #     "property": "firstname",
                    #     "value": request.POST.get('first_name')
                    # },
                    # {
                    #     "property": "lastname",
                    #     "value": request.POST.get('last_name')
                    # },
                    # {
                    #     "property": "company",
                    #     "value": "CodedBuzz"
                    # }
                ]
            })
            create_response = requests.post(url=endpoint, data=data, headers=headers)
            print(create_response.json())
        except:
            pass
    return TemplateResponse(request, 'hub_test/create_contact.html', context)



def check_for_existing_contacts(email='eyakuabsorkar@gmail.com'):
    endpoint = "https://api.hubapi.com/contacts/v1/contact/email/{}/profile?hapikey={}"\
        .format(email, settings.APP_API_KEY_TEST)
    check_response = requests.get(url=endpoint)
    print(check_response.status_code == 404)


def create_contact_property(property_name="order_amount"):
    endpoint = "https://api.hubapi.com/properties/v1/contacts/properties?hapikey={}".format(
        settings.APP_API_KEY_TEST
    )
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "name": property_name,
        "label": "Order Amount",
        "description": "A new property for you",
        "groupName": "contactinformation",
        "type": "string",
        "fieldType": "text",
        "formField": 'true',
        "displayOrder": 6,
        "options": [

        ]
    })
    response = requests.post(url=endpoint, data=data, headers=headers)
    print(response)


