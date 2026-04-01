import os
import requests
import time

token     = os.environ["IG_TOKEN"]
user_id   = os.environ["IG_USER_ID"]
video_url = os.environ["VIDEO_URL"]
caption   = os.environ["CAPTION"]

GRAPH_URL = "https://graph.facebook.com/v21.0"

print(f"Postando no Instagram: {video_url}")

r = requests.post(f"{GRAPH_URL}/{user_id}/media", params={
    "media_type":   "REELS",
    "video_url":    video_url,
    "caption":      caption,
    "access_token": token
})

if not r.ok:
    print(f"Erro ao criar container: {r.text}")
    exit(1)

container_id = r.json()["id"]
print(f"Container criado: {container_id}")

print("Aguardando processamento...")
for i in range(30):
    time.sleep(10)
    r2 = requests.get(f"{GRAPH_URL}/{container_id}", params={
        "fields": "status_code",
        "access_token": token
    })
    status = r2.json().get("status_code")
    print(f"Status: {status}")
    if status == "FINISHED":
        break
    if status == "ERROR":
        print("Erro no processamento!")
        exit(1)

r3 = requests.post(f"{GRAPH_URL}/{user_id}/media_publish", params={
    "creation_id":  container_id,
    "access_token": token
})

if not r3.ok:
    print(f"Erro ao publicar: {r3.text}")
    exit(1)

media_id = r3.json()["id"]
print(f"Publicado com sucesso! ID: {media_id}")
