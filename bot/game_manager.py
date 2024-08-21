import subprocess
import steam.webapi as steamapi
import os

class GameManager:
    def __init__(self, steam_path: Optional[str] = None):
        self.steam_path = steam_path or self.get_steam_path()

    def get_owned_games(api_key, steam_id):
        """Retrieve and store the owned games list for a user identified by their Steam ID."""
        steam_client = steamapi.WebAPI(api_key)
        owned_games = steam_client.IPlayerService.GetOwnedGames(
            steamid=steam_id,
            include_appinfo=True,
            include_played_free_games=True,
            appids_filter=[],
            include_free_sub=True,
            language='en',
            include_extended_appinfo=True
        )

        if 'games' in owned_games['response']:
            file_path = f"{steam_id}_games.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                for game in owned_games['response']['games']:
                    file.write(f"Game: {game['name']}, Steam ID: {game['appid']}\n")
            print(f"Game list saved to {file_path}")
        else:
            print("No games found or an error occurred.")

    def load_games_list(file_path):
        """Load the games and Steam IDs from the provided text file."""
        games = []
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Game:"):
                    parts = line.split(", Steam ID: ")
                    if len(parts) == 2:
                        game_name = parts[0].replace("Game: ", "").strip()
                        steam_id = parts[1].strip()
                        games.append({"name": game_name, "steam_id": steam_id})
        return games

    def compare_game_lists(game_lists, n=0):
        """Compare multiple game lists and find games common to all but n users."""
        from collections import Counter

        all_games = [game['name'] for games in game_lists for game in games]
        game_counter = Counter(all_games)
        total_users = len(game_lists)

        common_games = [game for game, count in game_counter.items() if count >= total_users - n]
        users_missing = {game: [i for i, games in enumerate(game_lists) if game not in [g['name'] for g in games]] for game in common_games}

        return common_games, users_missing

    def get_steam_path(self) -> str:
        if os.name == "nt":
            paths = [
                os.path.expandvars(r"%ProgramFiles(x86)%\Steam"),
                os.path.expandvars(r"%ProgramFiles%\Steam"),
                os.path.expandvars(r"%ProgramW6432%\Steam")
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        raise FileNotFoundError("Steam installation not found.")

    def launch_game(self, game_id: str, launch_options: Optional[str] = None) -> bool:
        process_name, game_name = get_running_game_process()
        if game_name:
            prompt_to_end_game(process_name, game_name)

        steam_path = get_steam_path()
        command = self.get_game_command(game_id, launch_options)
        try:
            subprocess.run(command, shell=True)
            print(f"Launched game: {game_id}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to launch game {game_id}: {e}")
            return False

    def get_running_game_process():
        process_list = subprocess.check_output("tasklist", shell=True).decode()
        known_games = {
            "Celeste.exe": "Celeste",
            "Brawlhalla.exe": "Brawlhalla",
            "Steam.exe": "Steam",
        }
        for process_name, game_name in known_games.items():
            if process_name in process_list:
                return process_name, game_name
        return None, None

    def prompt_to_end_game(process_name, game_name):
        prompt = input(f"{game_name} is currently running. Do you want to end the game? (y/n): ").strip().lower()
        if prompt == 'y':
            subprocess.run(f"taskkill /f /im {process_name}", shell=True)
            print(f"{game_name} has been closed.")
        else:
            print(f"{game_name} will continue running.")

    def get_game_command(self, game_id: str, launch_options: Optional[str] = None) -> str:
        commands = {
            "celeste": r'"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Celeste.exe"',
            "brawlhalla": r'"C:\Program Files (x86)\Steam\steamapps\common\Brawlhalla\Brawlhalla.exe"'
        }
        command = commands.get(game_id, "")
        if launch_options:
            command += f" {launch_options}"
        return command
