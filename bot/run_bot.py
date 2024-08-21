import yaml
from bot import lobby_manager
from bot.game_manager import get_owned_games, load_games_list, compare_game_lists

def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    api_key = config['steam']['api_key']
    friends = config['steam']['friends']

    # Generate game lists for each friend
    for friend in friends:
        steam_id = friend['steam_id']
        get_owned_games(api_key, steam_id)
    
    # Load all game lists
    game_lists = [load_games_list(f"{friend['steam_id']}_games.txt") for friend in friends]

    # Compare the game lists
    common_games, users_missing = compare_game_lists(game_lists, n=1)
    print("Games in common:", common_games)
    print("Users missing games:", users_missing)

if __name__ == "__main__":
    main()
    lobby_manager.main()
