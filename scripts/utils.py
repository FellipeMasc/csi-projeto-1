import pygame

import os

BASE_IMG_PATH = 'data/images/'

def load_image(path, resize=False):
    if resize:
        img = pygame.image.load(BASE_IMG_PATH + path)
        img = pygame.transform.scale(img, (35, 45))
        img_red = img.convert_alpha()
        return img_red
    
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img


def load_images(path):
    images = []
    resize = True if path[0:15] == "entities/player" or path[0:17] == "particles/sheldon" else False
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, resize))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

class HealthBar:
    def __init__(self, game, player, player_number):
        self.game = game
        self.player = player
        self.player_number = player_number
        self.width = 100
        self.height = 10
        self.border_width = 1
        self.x = 20 if player_number == 1 else 200
        self.y = 20

    def update(self):
        self.width = int((self.player.health / 100) * 100)

    def render(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), (self.x, self.y, self.width, self.height))

class EspecialBar:
    def __init__(self, game, player, player_number):
        self.game = game
        self.player = player
        self.player_number = player_number
        self.width = 0
        self.height = 5
        self.border_width = 1
        self.x = 20 if player_number == 1 else 200
        self.y = 30

    def update(self):
        self.width = int((self.player.stamina / 100) * 100)

    def render(self, surf):
        pygame.draw.rect(surf, (0, 0, 250), (self.x, self.y, self.width, self.height))


class Particles:
    def __init__(self, game, p_type,pos, player_number, velocity=[0,0], frame = 0, flip = False):
        self.game = game
        self.player_number = player_number
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame
        self.flip = flip
        
    
    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        self.animation.update()
        
        return kill
        
    def render(self, surf, offset=(0,0)):
        img = self.animation.img()
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
        
        
        
  

  
  
  
  
  
  
  
  
    
    
 

