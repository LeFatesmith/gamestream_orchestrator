import requests
import subprocess
import yaml

def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_lobby_id(api_key, friend_steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&format=json&steamids={friend_steam_id}"
    response = requests.get(url)
    data = response.json()

    if 'response' in data and 'players' in data['response']:
        player_info = data['response']['players'][0]
        game_id = player_info.get("gameid")
        lobby_id = player_info.get("lobbysteamid")

        if game_id and lobby_id:
            return game_id, lobby_id
        else:
            print("Game ID or Lobby ID not found in the API response.")
    else:
        print("API response did not contain the expected data.")
    return None, None

def join_friend_lobby(api_key, friend_steam_id):
    game_id, lobby_id = get_lobby_id(api_key, friend_steam_id)

    if game_id and lobby_id:
        join_command = f"steam://joinlobby/{game_id}/{lobby_id}/{friend_steam_id}"
        print(f"Attempting to join lobby with command: {join_command}")
        subprocess.run(['start', join_command], shell=True)
    else:
        print("Unable to join the friend's lobby.")

def main():
    config = load_config()
    steam_config = config['steam']
    api_key = steam_config['api_key']
    friends = steam_config['friends']

    for friend in friends:
        join_friend_lobby(api_key, friend['steam_id'])

if __name__ == "__main__":
    main()
