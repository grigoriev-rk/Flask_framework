import requests


# response = requests.post(
#     "http://127.0.0.1:5000/ads/",
#     json={
#         "title": "Ads_3",
#         "description": "Ads_3_description",
#         "owner": "User_3",
#     },)
# print(response.status_code)


response = requests.get('http://127.0.0.1:5000/ads/10')
print(response.status_code)
print(response.text)

response = requests.delete('http://127.0.0.1:5000/ads/11')
print(response.status_code)
print(response.text)



