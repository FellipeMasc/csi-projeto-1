import pygame
from game import Game
from Screen import Screen


class Editor:
    def __init__(self):
        pygame.init()
        self.play_again = False
        self.screen = pygame.display.set_mode((1280, 960))
    
    def run(self):
        tela = Screen(1280,960)
        if(self.play_again):
            tela.SelectionScreen(self.screen)
        else:
            tela.InitialScreen(self.screen)
        
        # game = Game(tela.P1sel, tela.P2sel, tela.map, self.screen)
        game = Game("coquinha", "farol", "maromba", self.screen)
        
        game.run()
        
        # tela.EndScreen(self.screen, game.winner)
        
        # game.cleanup()
        # del game
        # if(tela.play_again): 
        #     self.play_again = True
        #     self.run()

editor = Editor()
editor.run()