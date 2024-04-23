import sys
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from Screen import Screen


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ITA Fight Club")
        self.play_again = False
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((320, 240))
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        self.clock = pygame.time.Clock()

        self.movement_p1 = [False, False]
        self.movement_p2 = [False, False]
        # punch, kick, special, cokespecial
        self.attack_p1 = [False, False, False, False]
        self.attack_p2 = [False, False, False, False]
        self.block_p1 = False
        self.block_p2 = False
        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
            "background": load_image("background.png"),
            "particle/particle": Animation(load_images("particles/particle"), img_dur=6, loop=False),
            "player1/idle": Animation(load_images("entities/player/idle"), img_dur=6),
            "player1/run": Animation(load_images("entities/player/run"), img_dur=4),
            "player1/jump": Animation(load_images("entities/player/jump")),
            "player1/slide": Animation(load_images("entities/player/slide")),
            "player1/wall_slide": Animation(load_images("entities/player/wall_slide")),
            "player1/punch": Animation(load_images("entities/player/slide")),
            "player1/jump_attack": Animation(load_images("entities/player/slide")),
            "player1/kick": Animation(load_images("entities/player/wall_slide")),
            "player1/block": Animation(load_images("entities/player/wall_slide")),
            "player2/idle": Animation(load_images("entities/player/idle"), img_dur=6),
            "player2/run": Animation(load_images("entities/player/run"), img_dur=4),
            "player2/jump": Animation(load_images("entities/player/jump")),
            "player2/slide": Animation(load_images("entities/player/slide")),
            "player2/wall_slide": Animation(load_images("entities/player/wall_slide")),
            "player2/punch": Animation(load_images("entities/player/slide")),
            "player2/jump_attack": Animation(load_images("entities/player/slide")),
            "player2/kick": Animation(load_images("entities/player/wall_slide")),
            "player2/block": Animation(load_images("entities/player/wall_slide")),
        }

        self.player1 = Player(self, (50, 50), (8, 15), 1)
        self.player2 = Player(self, (100, 50), (8, 15), 2)

        self.tilemap = Tilemap(self, tile_size=16)
        self.particles = []

        self.scroll_1 = [0, 0]
        self.scroll_2 = [0, 0]

    def run(self):
        Tela = Screen(self.width, self.height)
        if (self.play_again):
            self.play_again = False
            Tela.SelectionScreen(self.screen)
        else:
            Tela.InitialScreen(self.screen)
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll_1[0] += (self.player1.rect().centerx - self.display.get_width() / 2 - self.scroll_1[0]) / 30
            self.scroll_1[1] += (self.player1.rect().centery - self.display.get_height() / 2 - self.scroll_1[1]) / 30
            self.scroll_2[0] += (self.player2.rect().centerx - self.display.get_width() / 2 - self.scroll_2[0]) / 30
            self.scroll_2[1] += (self.player2.rect().centery - self.display.get_height() / 2 - self.scroll_2[1]) / 30
            render_scroll = (
                int(min(self.scroll_1[0], self.scroll_2[0])),
                int(min(self.scroll_1[1], self.scroll_2[1])),
            )
            self.tilemap.render(self.display, offset=render_scroll)

            self.player1.render(self.display, offset=render_scroll)
            self.player1.update(
                self.tilemap,
                self.player2,
                self.attack_p1,
                (self.movement_p1[1] - self.movement_p1[0], 0),
                self.block_p1,
            )

            self.player2.render(self.display, offset=render_scroll)
            self.player2.update(
                self.tilemap,
                self.player1,
                self.attack_p2,
                (self.movement_p2[1] - self.movement_p2[0], 0),
                self.block_p2,
            )
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = render_scroll)
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_p1[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_p1[1] = True
                    if event.key == pygame.K_j:
                        self.attack_p1[0] = True
                    if event.key == pygame.K_k:
                        self.attack_p1[1] = True
                    if event.key == pygame.K_l:
                        self.player1.especial_attack(self)
                    if event.key == pygame.K_a:
                        self.movement_p2[0] = True
                    if event.key == pygame.K_d:
                        self.movement_p2[1] = True
                    if event.key == pygame.K_z:
                        self.attack_p2[0] = True
                    if event.key == pygame.K_x:
                        self.attack_p2[1] = True
                    if event.key == pygame.K_c:
                        self.player2.especial_attack(self)
                    if event.key == pygame.K_UP:
                        self.player1.jump()
                    if event.key == pygame.K_w:
                        self.player2.jump()
                    if event.key == pygame.K_n:
                        self.block_p1 = True
                    if event.key == pygame.K_v:
                        self.block_p2 = True
                    if event.key == pygame.K_f:
                        self.player1.dash()
                    if event.key == pygame.K_m:
                        self.player2.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_p1[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_p1[1] = False
                    if event.key == pygame.K_a:
                        self.movement_p2[0] = False
                    if event.key == pygame.K_d:
                        self.movement_p2[1] = False
                    if event.key == pygame.K_j:
                        self.attack_p1[0] = False
                    if event.key == pygame.K_k:
                        self.attack_p1[1] = False
                    if event.key == pygame.K_z:
                        self.attack_p2[0] = False
                    if event.key == pygame.K_x:
                        self.attack_p2[1] = False
                    if event.key == pygame.K_n:
                        self.block_p1 = False
                    if event.key == pygame.K_v:
                        self.block_p2 = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0),
            )
            pygame.display.update()
            self.clock.tick(60)
        
        
        

Game().run()
