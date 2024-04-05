import pygame
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                   entity_rect.right = rect.left
                   self.collisions['right'] = True
                if frame_movement[0] < 0:
                   entity_rect.left = rect.right 
                   self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                   entity_rect.bottom = rect.top
                   self.collisions['down'] = True
                if frame_movement[1] < 0:
                   entity_rect.top = rect.bottom
                   self.collisions['up'] = True 
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1]+ 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size, player_number):
        super().__init__(game, 'player{}'.format(player_number), pos, size)
        self.air_time = 0
        self.jumps = 1
        self.health = 100
        self.heath_bar = HealthBar(game, self, player_number)
    def update(self, tilemap, other_player, movement=(0,0)):
        super().update(tilemap, movement=movement)
        offset_bottom = 6
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        entity_rect = self.rect()
        if(entity_rect.colliderect(other_player.rect())):
            if frame_movement[0] > 0 and entity_rect.bottom > other_player.rect().top + offset_bottom:
                entity_rect.right = other_player.rect().left
                self.collisions['right'] = True
                self.pos[0] = entity_rect.x
            if frame_movement[0] < 0 and entity_rect.bottom > other_player.rect().top + offset_bottom:
                entity_rect.left = other_player.rect().right 
                self.collisions['left'] = True
                self.pos[0] = entity_rect.x
            if frame_movement[1] > 0 and entity_rect.top < other_player.rect().top:
                entity_rect.bottom = other_player.rect().top
                self.collisions['down'] = True
                self.pos[1] = entity_rect.y
            if frame_movement[1] < 0:
                self.collisions['up'] = True 


        
        
        self.air_time += 1
        if self.collisions['down']:
            print(self.air_time)
            self.air_time = 0
            self.jumps = 1
            

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
           self.wall_slide = True 
           self.velocity[1] = min(self.velocity[1], 0.5)
        
        print(self.action)
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
    def jump(self):
      if self.jumps:
              self.velocity[1] = -3
              self.jumps -= 1
              self.air_time = 5
    def render(self, surf, offset=(0, 0)):
        self.heath_bar.render(surf)
        return super().render(surf, offset)
              
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

