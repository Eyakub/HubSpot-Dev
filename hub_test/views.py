import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


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
    try:
        if request.method == 'POST':
            propUpdate = {
                "properties": [
                    {
                        "property": "favorite_book",
                        "value": request.body.new_val
                    }
                ]
            }
            apiCall = "https://api.hubspot.com/contacts/v1/contact/createOrUpdate/email/{}/profile?hapikey={}".format(
                email, settings.APP_API_KEY_TEST
            )
            try:
                update_response = requests.post(apiCall, propUpdate)
            except:
                pass
            return JsonResponse(update_response)
    except:
        pass
    context = {}
    return HttpResponse('hub_test/update_info.html', context)
