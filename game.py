import sys
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, HealthBar
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ITA Fight Club")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement_p1 = [False, False]
        self.movement_p2 = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'player1/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player1/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player1/jump': Animation(load_images('entities/player/jump')),
            'player1/slide': Animation(load_images('entities/player/slide')),
            'player1/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'player2/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player2/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player2/jump': Animation(load_images('entities/player/jump')),
            'player2/slide': Animation(load_images('entities/player/slide')),
            'player2/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        self.player1 = Player(self, (50, 50), (8, 15), 1)
        self.player2 = Player(self, (100, 50), (8, 15), 2)
        self.player1_health_bar = HealthBar(self, self.player1, 1)
        self.player2_health_bar = HealthBar(self, self.player2, 2)
        
        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player1.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player1.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)

            self.player1.update(self.tilemap, (self.movement_p1[1] - self.movement_p1[0], 0))
            self.player1.render(self.display, offset=render_scroll)
            self.player1_health_bar.update()
            self.player1_health_bar.render(self.display)

            self.player2.update(self.tilemap, (self.movement_p2[1] - self.movement_p2[0], 0))
            self.player2.render(self.display, offset=render_scroll)
            self.player2_health_bar.update()
            self.player2_health_bar.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_p1[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_p1[1] = True
                    if event.key == pygame.K_a:
                        self.movement_p2[0] = True
                    if event.key == pygame.K_d:
                        self.movement_p2[1] = True
                    if event.key == pygame.K_UP:
                        self.player1.jump()
                    if event.key == pygame.K_w:
                        self.player2.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_p1[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_p1[1] = False
                    if event.key == pygame.K_a:
                        self.movement_p2[0] = False
                    if event.key == pygame.K_d:
                        self.movement_p2[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()  # Refresh on-screen display
            self.clock.tick(60)  # wait until next frame (at 60 FPS)

Game().run()