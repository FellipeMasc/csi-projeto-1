import sys
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap


class Game:
    def __init__(self, player1_name, player2_name, map_name, screen):
        pygame.init()
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.map_name = map_name
        pygame.display.set_caption("ITA Fight Club")
        self.screen = screen
        self.display = pygame.Surface((320, 240))
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.winner = None
        self.movement_p1 = [False, False]
        self.movement_p2 = [False, False]
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
            "lago": load_image("lago.jpeg"),
            "salaonegro": load_image("salaonegro.jpeg"),
            # "background": load_image("background.png"),
            "particle/particle": Animation(load_images("particles/particle"), img_dur=6, loop=False),
            "particle/sheldon": Animation(load_images("particles/sheldon"), img_dur=6, loop=False),
            "player/farol/idle": Animation(load_images("entities/player/farol/idle"), img_dur=6),
            "player/farol/run": Animation(load_images("entities/player/farol/run"), img_dur=4),
            "player/farol/jump": Animation(load_images("entities/player/farol/jump")),
            "player/farol/punch": Animation(load_images("entities/player/farol/punch")),
            "player/farol/jump_attack": Animation(load_images("entities/player/farol/kick")),
            "player/farol/kick": Animation(load_images("entities/player/farol/kick")),
            "player/farol/block": Animation(load_images("entities/player/farol/block")),
            "player/farol/especial": Animation(load_images("entities/player/farol/especial"),img_dur=6, loop=False),
            "player/coquinha/idle": Animation(load_images("entities/player/coquinha/idle"), img_dur=6),
            "player/coquinha/run": Animation(load_images("entities/player/coquinha/run"), img_dur=4),
            "player/coquinha/jump": Animation(load_images("entities/player/coquinha/jump")),
            "player/coquinha/punch": Animation(load_images("entities/player/coquinha/punch")),
            "player/coquinha/jump_attack": Animation(load_images("entities/player/coquinha/kick")),
            "player/coquinha/kick": Animation(load_images("entities/player/coquinha/kick")),
            "player/coquinha/block": Animation(load_images("entities/player/coquinha/block")),
            "player/coquinha/especial": Animation(load_images("entities/player/coquinha/especial"),img_dur=6, loop=False),
            "player/calabresa/idle": Animation(load_images("entities/player/calabresa/idle"), img_dur=6),
            "player/calabresa/run": Animation(load_images("entities/player/calabresa/run"), img_dur=4),
            "player/calabresa/jump": Animation(load_images("entities/player/calabresa/jump")),
            "player/calabresa/punch": Animation(load_images("entities/player/calabresa/punch")),
            "player/calabresa/jump_attack": Animation(load_images("entities/player/calabresa/kick")),
            "player/calabresa/kick": Animation(load_images("entities/player/calabresa/kick")),
            "player/calabresa/block": Animation(load_images("entities/player/calabresa/block")),
            "player/calabresa/especial": Animation(load_images("entities/player/calabresa/especial"),img_dur=6, loop=False),
        }

        self.sfx = {
            'dash':pygame.mixer.Sound("data/sfx/dash.wav"),
            'especial/coquinha':pygame.mixer.Sound("data/sfx/coquinha-especial.wav"),
            'maromba':pygame.mixer.Sound("data/sfx/quertomarbomba.mp3"),
            'especial/farol':pygame.mixer.Sound("data/sfx/farol-especial.wav")
        }
        
        self.sfx["especial/coquinha"].set_volume(0.3)
        self.sfx["maromba"].set_volume(0.1)
        
        self.player1 = Player(self, (50, 50), (8, 15),1, self.player1_name)
        self.player2 = Player(self, (100, 50), (8, 15),2, self.player2_name)

        self.tilemap = Tilemap(self)
        self.particles = []

        self.scroll_1 = [0, 0]
        self.scroll_2 = [0, 0]

    
    def cleanup(self):
        pygame.mixer.music.stop()  
        pygame.mixer.quit()  
        
    def run(self):
        pygame.mixer.music.load("data/sfx/quertomarbomba.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        while True:
            self.display.blit(self.assets["salaonegro"], (0, 0))
            self.scroll_1[1] += (self.player1.rect().centery - self.display.get_height() / 3 - self.scroll_1[1]) / 10
            self.scroll_2[1] += (self.player2.rect().centery - self.display.get_height() / 3  - self.scroll_2[1]) / 10
            render_scroll = (
                0,
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
                    if event.key == pygame.K_p:
                        self.player1.plus(self)
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
                    if event.key == pygame.K_q:
                        self.player2.plus(self)
                    if event.key == pygame.K_UP:
                        self.player1.jump()
                    if event.key == pygame.K_w:
                        self.player2.jump()
                    if event.key == pygame.K_n:
                        self.block_p1 = True
                    if event.key == pygame.K_v:
                        self.block_p2 = True
                    if event.key == pygame.K_m:
                        self.player1.dash()
                    if event.key == pygame.K_f:
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

            if(self.player1.die):
                self.winner = 2
                break
            
            if(self.player2.die):
                self.winner = 1;
                break
                
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0),
            )
            pygame.display.update()
            self.clock.tick(60)
        
    def __del__(self):
        print("Instância deletada!")
        
