# import json
# from zoomus import ZoomClient
#
# def generate_zoom(request):
#
#         #spain1292 account
#         # client = ZoomClient('1bFDBicDQxmSAZbECE5P_Q', 'MxnnAokQjG3vhiiTqh1lYDvL20mS4gmOIOmh', version=2)
#         #wsu project account
#         client = ZoomClient('u3JZMoifS5euyc_gQDWVGw', 'IZ3qfz9sf2WQVWvxCF5RxZyfFrXP6TThXD1t', version=2)
#
#
#         user_list_response = client.user.list()
#         user_list = json.loads(user_list_response.content)
#
#
#         for user in user_list['users']:
#             user_id = user['id']
#
#             #creates a meeting
#             #client.meeting.create(user_id=user_id)
#
#
#             meetings=(json.loads(client.meeting.list(user_id=user_id, page_size='5',page_number='1').content))
#             # print(meetings['meetings'][-1]['join_url'])
#
#             # print(meetings['page_count'])
#             # assining last page number to the variable (page_count returns total number of pages, which is same as last page number
#             last_page_number = meetings['page_count']
#             fetch_last_meeting = (json.loads(client.meeting.list(user_id=user_id, page_size='5',page_number=last_page_number).content))
#             print(fetch_last_meeting)
#             meeting_url = fetch_last_meeting['meetings'][-1]['join_url']
#             print(meeting_url)
#             count = 0
#             for m in fetch_last_meeting['meetings']:
#                 print(m['join_url'])
#                 # client.meeting.delete(meeting_id=m['uuid'])
#                 count = count + 1
#                 print(count)
#
#             return meeting_url
#
#
# generate_zoom(request=1)
#
#
