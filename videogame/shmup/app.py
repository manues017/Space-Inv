import pygame
from moviepy.editor import VideoFileClip
from states.statemanager import StateManager
from config import cfg_item

class App:
    def __init__(self):
        """
        Initializes the application, sets up the display, loads the background video and music, and initializes the state manager.
        """
        pygame.init()
        self.__screen = pygame.display.set_mode(cfg_item("game", "screen_size"), pygame.RESIZABLE, 32)
        pygame.display.set_caption("My Super Videogame!!!")
        pygame.mouse.set_visible(False)
        
        video_path = cfg_item("game", "background_video")
        self.__video = VideoFileClip(video_path)
        self.__video_iterator = iter(self.__video.iter_frames(fps=30, with_times=False))

        pygame.mixer.init()
        self.__load_music(cfg_item("game", "background_music"))

        self.__clock = pygame.time.Clock()
        self.__state_manager = StateManager()

    def run(self):
        """
        Starts the main application loop.
        """
        self.__running = True

        while self.__running:
            delta_time = self.__clock.tick(60)
            self.__process_events()
            self.__update(delta_time)
            self.__render()

        self.__release()

    def __process_events(self):
        """
        Processes all events from the event queue.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.__state_manager.get_state().next_state == "Exit":
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
            self.__state_manager.process_events(event)

    def __update(self, delta_time):
        """
        Updates the current state.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        self.__state_manager.update(delta_time)

    def __render(self):
        """
        Renders the current state and the video background.
        """
        self.__play_video_background()
        self.__state_manager.render(self.__screen)
        pygame.display.update()
        
    def __play_video_background(self):
        """
        Plays the video background frame by frame.
        """
        try:
            frame = next(self.__video_iterator)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.__screen.blit(frame_surface, (0, 0))
        except StopIteration:
            self.__video_iterator = iter(self.__video.iter_frames(fps=30, with_times=False))
            frame = next(self.__video_iterator)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.__screen.blit(frame_surface, (0, 0))
            
    def __load_music(self, music_file):
        """
        Loads and plays background music.

        Args:
            music_file (str): The path to the music file.
        """
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)  # Adjusts volume between 0.0 and 1.0
        pygame.mixer.music.play(-1)  # Loops the music indefinitely

    def __release(self):
        """
        Releases resources and quits the application.
        """
        self.__state_manager.release()
        self.__video.close()  # Close the video
        pygame.quit()