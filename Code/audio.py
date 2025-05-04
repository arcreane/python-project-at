import pygame

class AudioManager:
    def __init__(self, music_by_map: dict):
        pygame.mixer.init()
        self.music_by_map = music_by_map
        self.current_music = None

    def play_for_map(self, map_name: str):
        music_path = self.music_by_map.get(map_name)

        if music_path is None:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                self.current_music = None
            return

        if self.current_music == music_path:
            return

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loops=-1)
        self.current_music = music_path

    def stop(self):
        pygame.mixer.music.stop()
        self.current_music = None
