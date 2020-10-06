from django.urls import path, include
from hub_test.views import index, individual_data, create_contact, contact_property_info


app_name = 'hub_test'

urlpatterns = [
    path('', index, name='index'),
    path('user_info/', contact_property_info, name='individual-data'),
    path('create_contact', create_contact, name='create-contact'),
]
