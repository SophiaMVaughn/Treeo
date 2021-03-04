# import json
# from zoomus import ZoomClient
#
#
# def generate_zoom(request):
#
#         client = ZoomClient('u3JZMoifS5euyc_gQDWVGw', 'tHXyCqfu8YCTbe52taSKTffzEilKQmPmj8rU',version=2)
#
#         user_list_response = client.user.list()
#         user_list = json.loads(user_list_response.content)
#         # print(create_meeting_resp)
#
#
#         # print(json.loads(user_list_response.content))
#
#         for user in user_list['users']:
#             user_id = user['id']
#             print(user_id)
#             create_meeting_resp = client.meeting.create(user_id=user_id)
#             print('\n')
#             # print(json.loads(client.meeting.list(user_id=user_id).content))
#             meetings=(json.loads(client.meeting.list(user_id=user_id).content))
#             # print(meetings['meetings'][-1]['join_url'])
#             meeting_url = meetings['meetings'][-1]['join_url']
#             print(meeting_url)
#             # for m in meetings['meetings']:
#             #     print(m['join_url'])
#         #
#         # print(meeting_url)
#         # print('###########################')
#         #         # return meeting_url
#
#
#
# generate_zoom(request=1)
# zoom_meeting_link = generate_zoom(request=1)
# print(zoom_meeting_link)
