import requests

st_time=int(input())
end_time=int(input())

json_data = {}
json_data['st_time'] = st_time
json_data['end_time'] = end_time

response = requests.get('http://localhost:8000/getVehicleInfo', json=json_data).content
print(response)

