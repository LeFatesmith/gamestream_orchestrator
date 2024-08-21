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
        command = self.get_game_command(game_id, launch_options)
        try:
            subprocess.run(command, shell=True)
            print(f"Launched game: {game_id}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to launch game {game_id}: {e}")
            return False

    def get_game_command(self, game_id: str, launch_options: Optional[str] = None) -> str:
        commands = {
            "celeste": r'"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Celeste.exe"',
            "brawlhalla": r'"C:\Program Files (x86)\Steam\steamapps\common\Brawlhalla\Brawlhalla.exe"'
        }
        command = commands.get(game_id, "")
        if launch_options:
            command += f" {launch_options}"
        return command
