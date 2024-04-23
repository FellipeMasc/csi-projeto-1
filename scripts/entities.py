import sys
import pygame
from .utils import HealthBar, EspecialBar, Particles


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {
            "up": False,
            "down": False,
            "right": False,
            "left": False,
        }

        self.action = ""
        self.anim_offset = (-10, -30)
        self.flip = False
        self.set_action("idle")

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + "/" + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {
            "up": False,
            "down": False,
            "right": False,
            "left": False,
        }

        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - offset[0] + self.anim_offset[0],
                self.pos[1] - offset[1] + self.anim_offset[1],
            ),
        )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size, player_number, player_name):
        super().__init__(game, "player/" +player_name, pos, size)
        self.air_time = 0
        self.jumps = 1
        self.health = 100
        self.stamina = 0
        self.melee_attack = False
        self.block = False
        self.especial_frame = False
        self.dashing = 0
        self.player_number = player_number
        self.heath_bar = HealthBar(game, self, player_number)
        self.especial_bar = EspecialBar(game,self,player_number)
        self.impact_force = 2
        self.player_name = player_name

    def update(
        self,
        tilemap,
        other_player,
        attack=[False, False, False, False],
        movement=(0, 0),
        block=False,
    ):
        super().update(tilemap, movement=movement)
        offset_bottom = 6
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )
        entity_rect = self.rect()
        other_rect = other_player.rect()
        if abs(entity_rect.left - other_rect.right) < 3 or abs(entity_rect.right - other_rect.left) < 3:
            if other_player.melee_attack and abs(entity_rect.top - other_rect.top) < 8 and not self.block:
                self.health = self.health - 1
                other_player.stamina = min(100,other_player.stamina + 3)
                if other_player.flip:
                   self.velocity[0] -= self.impact_force/10
                else:
                   self.velocity[0] += self.impact_force/10
                self.heath_bar.update()
                other_player.especial_bar.update()
                
                
                
        self.anim_offset = (-13,-30)
        if entity_rect.colliderect(other_rect):
            if frame_movement[0] > 0 and entity_rect.bottom > other_rect.top + offset_bottom:
                entity_rect.right = other_rect.left
                self.collisions["right"] = True
                self.pos[0] = entity_rect.x
            if frame_movement[0] < 0 and entity_rect.bottom > other_rect.top + offset_bottom:
                entity_rect.left = other_rect.right
                self.collisions["left"] = True
                self.pos[0] = entity_rect.x
            if frame_movement[1] > 0 and entity_rect.top < other_rect.top:
                entity_rect.bottom = other_rect.top
                self.collisions["down"] = True
                self.pos[1] = entity_rect.y
                self.anim_offset = (-10,-60);
            if frame_movement[1] < 0:
                self.collisions["up"] = True

        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 2
        self.wall_slide = False
        if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            
            
        if self.air_time > 4:
            if attack[0] or attack[1]:
                self.set_action("jump_attack")
            else:
                self.set_action("jump")
        elif movement[0] != 0:
            self.set_action("run")
        elif attack[0]:
            self.set_action("punch")
        elif attack[1]:
            self.set_action("kick")
        elif block:
            self.set_action("block")
        elif self.especial_frame and not self.animation.done:
            self.set_action("especial")
        else:
            self.especial_frame = False
            self.set_action("idle")

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
            
        for particle in self.game.particles:
            new_rect = pygame.Rect(
                        self.rect().left,
                        self.rect().top - 40,
                        8,
                        40,
                    )
            if new_rect.collidepoint(particle.pos) and particle.player_number != self.player_number and not self.block:
                if particle.type != 'sheldon':
                    if other_player.flip:
                        self.velocity[0] -= self.impact_force * 2
                    else:
                        self.velocity[0] += self.impact_force * 2
                self.health = self.health - 5
                self.heath_bar.update()
                self.game.particles.remove(particle)
        

    def set_action(self, action):
        self.melee_attack = ["punch", "kick", "jump_attack"].count(action) > 0
        self.block = action == "block"
        return super().set_action(action)

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
                
                
    def especial_attack(self, game):
        if(self.stamina == 100):
            velocityx = -5 if self.flip else 5
            game.particles.append(Particles(game,'particle', [self.rect().centerx, self.rect().centery - 30],self.player_number, [velocityx, 0]))
            self.stamina = 0
            self.especial_bar.update()
            self.especial_frame = True
            

    def render(self, surf, offset=(0, 0)):
        self.heath_bar.render(surf)
        self.especial_bar.render(surf)
        return super().render(surf, (offset[0], offset[1] ))
    
    def plus(self,game):
        if(self.stamina == 0 and self.player_name == "coquinha"):
            other_player = game.player2 if self.player_number == 1 else game.player1
 
            
            velocityx = -5 if self.flip else 5
            game.particles.append(Particles(game,'sheldon', [other_player.rect().centerx -12, other_player.rect().centery - 20],self.player_number, [0.2, 0],0, False))
            game.particles.append(Particles(game,'sheldon', [other_player.rect().centerx +12, other_player.rect().centery - 20],self.player_number, [-0.2, 0],0, True))
            self.stamina = 0
            self.especial_bar.update()
            self.especial_frame = True


        
    