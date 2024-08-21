def test_get_steam_path(self):
    path = get_steam_path()
    self.assertTrue(os.path.exists(path))

def test_get_running_game_process(self):
    process_name, game_name = get_running_game_process()
    self.assertIn(process_name, ["Celeste.exe", "Brawlhalla.exe", None])

def test_prompt_to_end_game(self):
    prompt_to_end_game("Steam.exe", "Steam")
    # This can be more detailed based on user input simulation
