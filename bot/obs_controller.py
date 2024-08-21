import subprocess

class OBSController:
    def __init__(self, obs_path: Optional[str] = None):
        self.obs_path = obs_path or r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"

    def change_scene(self, scene_name: str) -> bool:
        command = f'{self.obs_path} --scene "{scene_name}"'
        try:
            subprocess.run(command, shell=True)
            print(f"Changed OBS scene to {scene_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to change scene: {e}")
            return False
