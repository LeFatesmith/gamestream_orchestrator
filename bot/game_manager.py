import subprocess
import os

class GameManager:
    def __init__(self, steam_path: Optional[str] = None):
        self.steam_path = steam_path or self.get_steam_path()

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
