import requests
import json
import time
import os

TOKEN = "YOUR_TOKEN_HERE"
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}
API_URL = "https://discord.com/api/v9"

def get_data(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}", headers=HEADERS)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return f"Erreur {response.status_code}: Réponse JSON invalide"
    return f"Erreur {response.status_code}: {response.text}"

def get_all_messages(channel_id, limit=1000):
    messages = []
    last_message_id = None
    while len(messages) < limit:
        url = f"channels/{channel_id}/messages?limit=100"
        if last_message_id:
            url += f"&before={last_message_id}"
        batch = get_data(url)
        if not isinstance(batch, list):
            break
        messages.extend(batch)
        if len(batch) < 100:
            break
        last_message_id = batch[-1]['id']
        time.sleep(1)
    return messages

def save_json(directory, filename, data):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def progress_bar(current, total, bar_length=40):
    progress = int((current / total) * bar_length)
    bar = "█" * progress + "-" * (bar_length - progress)
    print(f"[{bar}] {current}/{total} ({(current / total) * 100:.2f}%)", end="\r")

# Demande le nom du dossier de sortie
output_directory = input("Nom du dossier pour stocker les fichiers JSON : ")

# Récupération des données principales
tasks = [
    ("user_info.json", "users/@me"),
    ("guilds.json", "users/@me/guilds"),
    ("friends.json", "users/@me/relationships"),
    ("connections.json", "users/@me/connections"),
    ("billing.json", "users/@me/billing/payment-sources"),
    ("sessions.json", "users/@me/sessions"),
    ("settings.json", "users/@me/settings"),
    ("boosts.json", "users/@me/guilds/premium/subscriptions"),
    ("login_history.json", "users/@me/sessions")
]

total_tasks = len(tasks)
completed_tasks = 0

for filename, endpoint in tasks:
    data = get_data(endpoint)
    if isinstance(data, (dict, list)):
        save_json(output_directory, filename, data)
    else:
        print(f"Erreur: Données invalides reçues pour {endpoint}: {data}")
    completed_tasks += 1
    progress_bar(completed_tasks, total_tasks)

# Récupération des messages privés + pseudos et avatars
dms = get_data("users/@me/channels")
all_dm_messages = {}

if isinstance(dms, list):
    for dm in dms:
        if isinstance(dm, dict):
            user_info = dm.get("recipients", [{}])[0]
            user_data = {
                "id": user_info.get("id"),
                "username": user_info.get("username"),
                "avatar": f"https://cdn.discordapp.com/avatars/{user_info.get('id')}/{user_info.get('avatar')}.png"
            }
            messages = get_all_messages(dm.get('id', ''), limit=1000)
            all_dm_messages[dm.get('id', '')] = {"user": user_data, "messages": messages}
            save_json(output_directory, "dm_messages.json", all_dm_messages)
            completed_tasks += 1
            progress_bar(completed_tasks, total_tasks + len(dms))
        else:
            print(f"Erreur: dm n'est pas un dictionnaire, valeur reçue: {dm}")
else:
    print(f"Erreur: Liste des DMs non valide: {dms}")

# Récupération des membres et messages des serveurs
guilds = get_data("users/@me/guilds")
all_server_messages = {}

if isinstance(guilds, list):
    for guild in guilds:
        if isinstance(guild, dict):
            guild_id = guild.get('id', '')
            channels = get_data(f"guilds/{guild_id}/channels")
            members = get_data(f"guilds/{guild_id}/members?limit=1000")
            
            if not isinstance(members, list):
                print(f"Erreur: Liste des membres non valide pour {guild.get('name', 'Serveur inconnu')}")
                members = []
            
            server_data = {
                "guild_name": guild.get("name"),
                "guild_id": guild_id,
                "members": [
                    {
                        "id": member["user"]["id"],
                        "username": member["user"].get("username", ""),
                        "avatar": f"https://cdn.discordapp.com/avatars/{member['user']['id']}/{member['user'].get('avatar', '')}.png",
                        "roles": member.get("roles", [])
                    }
                    for member in members if isinstance(member, dict) and "user" in member
                ],
                "messages": {}
            }
            
            if isinstance(channels, list):
                for channel in channels:
                    if isinstance(channel, dict) and channel.get('type') == 0:
                        messages = get_all_messages(channel.get('id', ''), limit=1000)
                        server_data["messages"][channel.get('id', '')] = messages
            else:
                print(f"Erreur: Liste des salons non valide pour {guild.get('name', 'Serveur inconnu')}")
            
            all_server_messages[guild_id] = server_data
            save_json(output_directory, "server_messages.json", all_server_messages)
            completed_tasks += 1
            progress_bar(completed_tasks, total_tasks + len(dms) + len(guilds))
        else:
            print(f"Erreur: guild n'est pas un dictionnaire, valeur reçue: {guild}")
else:
    print(f"Erreur: Liste des serveurs non valide: {guilds}")

print("\nExtraction terminée !")
