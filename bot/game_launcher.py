import subprocess

def load_games_list(file_path):
    """Load the games and Steam IDs from the provided text file."""
    games = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Game:"):
                parts = line.split(", Steam ID: ")
                if len(parts) == 2:
                    game_name = parts[0].replace("Game: ", "").strip()
                    steam_id = parts[1].strip()
                    games.append({"name": game_name, "steam_id": steam_id})
    return games

def find_game_by_name(games, game_name):
    """Find a game by name (case-insensitive) in the games list."""
    for game in games:
        if game_name.lower() in game["name"].lower():
            return game
    return None

def launch_game(game, launch_options=None):
    """Launch a game using its Steam ID and optional launch options."""
    steam_id = game["steam_id"]
    base_command = f"start steam://launch/{steam_id}"
    
    if launch_options:
        base_command += f"/{launch_options}"

    # Execute the command to launch the game
    subprocess.run(base_command, shell=True)

def main():
    # Load games list from the file
    file_path = "out.txt"
    games_list = load_games_list(file_path)
    
    # Example user input
    game_name = input("Enter the name of the game you want to launch: ").strip()
    
    # Find the game in the list
    game = find_game_by_name(games_list, game_name)
    
    if game:
        print(f"Launching {game['name']} (Steam ID: {game['steam_id']})...")
        # Optional: Include additional launch options
        launch_options = input("Enter additional launch options (or press Enter to skip): ").strip()
        launch_game(game, launch_options if launch_options else None)
    else:
        print("Game not found in your list.")

if __name__ == "__main__":
    main()
