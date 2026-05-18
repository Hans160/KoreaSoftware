import requests

url = "https://api.github.com/users/lovehyun/repos"

resp = requests.get(url)
repos = resp.json()

# print(repos)
data =[]

for repo in repos:
    name = repo["name"]
    html_url = repo["html_url"]
    description = repo["description"]
    data.append({
        "리포이름": name,
        "리포url": html_url,
        "설명": description
    })

for d in data:
    print(d)    
    
