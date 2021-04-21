import json
from zoomus import ZoomClient
from django.conf import settings
import json
import random
import string



	#Author: Giorgi Nozadze
	#This method generates the zoom link by using zoom provided credentials, zoom API is ran using wrapper called zoomus


def generate_zoom(request):

    #todo- Hey everyone, if you get req per second error form zoom that means account is exhausted
    #todo - just switch to second account, all you have to do is comment out the line 21
    #todo - please don't change anything in this code

    #spain1292 account
    client = ZoomClient('1bFDBicDQxmSAZbECE5P_Q', 'MxnnAokQjG3vhiiTqh1lYDvL20mS4gmOIOmh', version=2)
    #wsu project account
    # client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_SECRET_KEY, version=2)


    user_list_response = client.user.list()
    user_list = json.loads(user_list_response.content)



      # print(json.loads(user_list_response.content))

    for user in user_list['users']:
        user_id = user['id']

        # creates a meeting
        create_response = client.meeting.create(user_id=user_id, password=''.join(
            random.choice(string.ascii_lowercase) for i in range(0)))
        if create_response.status_code != 201:
            return 0
        else:
            resp_json = json.loads(create_response.content)
            provider_url = resp_json['start_url']
            patient_url = resp_json['join_url']
            patient_pwd = resp_json['password']

        print(create_response.content)

        for i, j in json.loads(create_response.content).items():
            print(i, j)

        return [provider_url, patient_url,patient_pwd]

        # meetings = (json.loads(client.meeting.list(user_id=user_id, page_size='5', page_number='1').content))
        # # print(meetings['meetings'][-1]['join_url'])
        # print(meetings)
        # # print(meetings['page_count'])
        # # assining last page number to the variable (page_count returns total number of pages, which is same as last page number
        # last_page_number = meetings['page_count']
        # fetch_last_meeting = (
        #     json.loads(client.meeting.list(user_id=user_id, page_size='5', page_number=last_page_number).content))
        # print(fetch_last_meeting)
        # meeting_url = fetch_last_meeting['meetings'][-1]['join_url']
        # print(meeting_url)
        # count = 0
        # for m in fetch_last_meeting['meetings']:
        #     print(m['join_url'])
        #     # client.meeting.delete(meeting_id=m['uuid'])
        #     count = count + 1
        #     print(count)
        #
        # return meeting_url


