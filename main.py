import pygame
from noise_handler import Noise_Handler
from numpy import array
import numpy as np
from noise_loop import get_polar_noise_2d


class App:
    # main function from where everything is called
    def __init__(self):
        # initiating a clock and setting timer of the application
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.time_per_frame = 1000 / self.fps

        self._running = True
        self.display: pygame.display = None

        self.noise_frames = 10

        self.size = array([500, 500])

        self.noise = get_polar_noise_2d(self.noise_frames, self.size, 0.03, detail=8)
        self.noise2 = get_polar_noise_2d(self.noise_frames, self.size, 0.03, detail=10)

        self.png_path = "pngs/"

    # called once to start program
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.on_execute()

    # handles player inputs
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    # loop which will be executed at fixed rate (for physics, animations and such)
    def on_loop(self):
        pass

    # loop which will only be called when enough cpu time is available
    def on_render(self):
        self.display.fill((30, 144, 255))

        for i in range(self.noise_frames):
            self.draw_water(self.noise[i], self.noise2[i])
            path = f"{self.png_path}layer{i}.png"
            pygame.image.save(self.display, path)

        pygame.display.update()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        previous = pygame.time.get_ticks()
        lag = 0.0

        # advanced game loop to call on_loop() at fixed rate and on_render() as fast as possible
        # (kinda overkill right now) (also not relevant)
        while self._running:
            current = pygame.time.get_ticks()
            elapsed = current - previous
            lag += elapsed
            previous = current

            for event in pygame.event.get():
                self.on_event(event)

            while lag > self.time_per_frame:
                self.on_loop()
                lag -= self.time_per_frame
            self.on_render()
        self.on_cleanup()

    def draw_water(self, noise_layer, noise_layer2):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                val = noise_layer[i][j]
                val2 = noise_layer2[i][j]
                match val:
                    case _ if val > 0.15:
                        color = (135, 206, 250)

                    case _:
                        if -0.05 < val2 < 0.05:
                            color = (200, 200, 255)
                        else:
                            color = (30, 144, 255)
                self.display.set_at((i, j), color)
            pygame.display.update()


if __name__ == "__main__":
    app = App()
    app.on_init()
