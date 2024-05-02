import pygame
import sys

class Screen:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.ready = False
        self.P1sel = ""
        self.P2sel = ""
        self.map = ""
        self.play_again = False
        self.ready = False

    def draw_initial_buttons(self, screen):
        button_width, button_height = 300, 80
        button_padding = 20

        # Botão 1
        button1_rect = pygame.Rect((self.width - button_width) // 2, self.height // 2 - button_height + 6*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button1_rect)
        pygame.draw.rect(screen, self.black, button1_rect, 2)

        font = pygame.font.SysFont(None, 32)
        text = font.render("Clique para jogar", True, self.black)
        text_rect = text.get_rect(center=button1_rect.center)
        screen.blit(text, text_rect)

        # Botão 2
        button2_rect = pygame.Rect((self.width - button_width) // 2, self.height // 2 + 7*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button2_rect)
        pygame.draw.rect(screen, self.black, button2_rect, 2)

        text = font.render("Entenda como jogar", True, self.black)
        text_rect = text.get_rect(center=button2_rect.center)
        screen.blit(text, text_rect)

        return button1_rect, button2_rect
    
    def draw_selection_buttons(self, screen):
        button_width, button_height = 180, 180
        button_spacing = 20
        button_image1 = pygame.image.load("imagens_tela_inicial/coquinha.jpg")
        button_image1 = pygame.transform.scale(button_image1, (button_width, button_height))
        button_image2 = pygame.image.load("imagens_tela_inicial/calacala.jpg")
        button_image2 = pygame.transform.scale(button_image2, (button_width, button_height))
        button_image3 = pygame.image.load("imagens_tela_inicial/farol.jpg")
        button_image3 = pygame.transform.scale(button_image3, (button_width, button_height))
        button_image4 = pygame.image.load("imagens_tela_inicial/rinha.jpg")
        button_image4 = pygame.transform.scale(button_image4, (button_width, button_height))
        buttons = []

        # Calculando a posição dos botões
        button_positions = [
            (self.width/4 - button_spacing/2 - button_width, self.height/2 - button_spacing/2 - button_height + 30),
            (3*self.width/4 + button_spacing/2, self.height/2 - button_spacing/2 - button_height + 30),
            (self.width/4 - button_spacing/2 - button_width, self.height/2 + button_spacing/2 + 30),
            (3*self.width/4 + button_spacing/2, self.height/2 + button_spacing/2 + 30),
            (self.width/4 + button_spacing/2, self.height/2 - button_spacing/2 - button_height + 30),
            (3*self.width/4 - button_spacing/2 - button_width, self.height/2 - button_spacing/2 - button_height + 30),
            (self.width/4 + button_spacing/2, self.height/2 + button_spacing/2 + 30),
            (3*self.width/4 - button_spacing/2 - button_width, self.height/2 + button_spacing/2 + 30)
        ]

        i = 0
        for pos in button_positions:
            button_rect = pygame.Rect(pos[0], pos[1], button_width, button_height)
            pygame.draw.rect(screen, self.gray, button_rect)
            pygame.draw.rect(screen, self.black, button_rect, 2)
            if i == 0 or i == 5:
                image_rect = button_image1.get_rect(center=button_rect.center)
                screen.blit(button_image1, image_rect)
            elif i == 1 or i == 4:
                image_rect = button_image2.get_rect(center=button_rect.center)
                screen.blit(button_image2, image_rect)
            elif i == 2 or i == 7:
                image_rect = button_image3.get_rect(center=button_rect.center)
                screen.blit(button_image3, image_rect)
            else:
                image_rect = button_image4.get_rect(center=button_rect.center)
                screen.blit(button_image4, image_rect) 
            i = i + 1
            buttons.append(button_rect)

        return buttons
    
    def draw_tutorial_button(self, screen):
        button_width, button_height = 300, 60
        button_padding = 20

        # Botão 1
        button_rect = pygame.Rect((self.width - button_width) // 2, self.height // 2 - button_height + 10*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button_rect)
        pygame.draw.rect(screen, self.black, button_rect, 2)

        font = pygame.font.SysFont(None, 32)
        text = font.render("Clique para retornar", True, self.black)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        return button_rect

    def draw_map_buttons(self, screen):
        button_width, button_height = 200, 60
        button_padding = 10

        # Botão 1
        button1_rect = pygame.Rect((self.width - button_width) // 2 - button_width - button_padding, self.height // 2 - button_height + 6*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button1_rect)
        pygame.draw.rect(screen, self.black, button1_rect, 2)

        font = pygame.font.SysFont(None, 32)
        text = font.render("Salão Negro", True, self.black)
        text_rect = text.get_rect(center=button1_rect.center)
        screen.blit(text, text_rect)

        # Botão 2
        button2_rect = pygame.Rect((self.width - button_width) // 2, self.height // 2 - button_height + 6*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button2_rect)
        pygame.draw.rect(screen, self.black, button2_rect, 2)

        text = font.render("Maromba", True, self.black)
        text_rect = text.get_rect(center=button2_rect.center)
        screen.blit(text, text_rect)

        # Botão 3
        button3_rect = pygame.Rect((self.width - button_width) // 2 + button_width + button_padding, self.height // 2 - button_height + 6*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button3_rect)
        pygame.draw.rect(screen, self.black, button3_rect, 2)

        text = font.render("Lago", True, self.black)
        text_rect = text.get_rect(center=button3_rect.center)
        screen.blit(text, text_rect)

        # Botão 4
        button4_rect = pygame.Rect((self.width - button_padding) // 2 - button_width, self.height // 2 - button_height + 20*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button4_rect)
        pygame.draw.rect(screen, self.black, button4_rect, 2)

        text = font.render("Voltar", True, self.black)
        text_rect = text.get_rect(center=button4_rect.center)
        screen.blit(text, text_rect)

        # Botão 5
        button5_rect = pygame.Rect((self.width + button_padding) // 2, self.height // 2 - button_height + 20*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button5_rect)
        pygame.draw.rect(screen, self.black, button5_rect, 2)

        text = font.render("Começar", True, self.black)
        text_rect = text.get_rect(center=button5_rect.center)
        screen.blit(text, text_rect)

        return button1_rect, button2_rect, button3_rect, button4_rect, button5_rect
    
    def draw_end_buttons(self, screen):
        button_width, button_height = 200, 60
        button_padding = 10
        # Botão 1
        button1_rect = pygame.Rect((self.width - button_padding) // 2 - button_width, self.height // 2 - button_height + 20*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button1_rect)
        pygame.draw.rect(screen, self.black, button1_rect, 2)

        font = pygame.font.SysFont(None, 32)
        text = font.render("Jogar novamente", True, self.black)
        text_rect = text.get_rect(center=button1_rect.center)
        screen.blit(text, text_rect)

        # Botão 5
        button2_rect = pygame.Rect((self.width + button_padding) // 2, self.height // 2 - button_height + 20*button_padding, button_width, button_height)
        pygame.draw.rect(screen, self.gray, button2_rect)
        pygame.draw.rect(screen, self.black, button2_rect, 2)

        text = font.render("Encerrar", True, self.black)
        text_rect = text.get_rect(center=button2_rect.center)
        screen.blit(text, text_rect)

        return button1_rect, button2_rect

    def SelectionScreen(self, screen):
        screen.fill(self.white)
        image_sel = pygame.image.load("imagens_tela_inicial/tela_de_selecao.jpg")
        image_sel = pygame.transform.scale(image_sel, (self.width, self.height))
        image_sel_rect = image_sel.get_rect()
        screen.blit(image_sel, ((self.width - image_sel_rect.width) // 2, (self.height - image_sel_rect.height) // 2))
        pygame.display.flip()
        mouse_over_button = False
        button_rects = self.draw_selection_buttons(screen)
        running = True
        button_selected = []
        P1_buttons = [0, 4, 2, 6]
        P2_buttons = [3, 5, 1, 7]
        
        self.sfx = {
            'coquinha':pygame.mixer.Sound("data/sfx/coquinha-especial-plus.wav"),
            'calabresa':pygame.mixer.Sound("data/sfx/calabresa-inicio.wav"),
            'rinha':pygame.mixer.Sound("data/sfx/rinha-inicio.wav"),
            'farol':pygame.mixer.Sound("data/sfx/farol-inicio.wav"),
        }
        
        self.sfx['coquinha'].set_volume(0.4)
        self.sfx['calabresa'].set_volume(0.4)
        self.sfx['rinha'].set_volume(0.4)
        self.sfx['farol'].set_volume(0.4)
        
        
        for _ in range(len(button_rects)):
            button_selected.append(False)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for rect in button_rects:
                        if rect.collidepoint(mouse_pos):
                            mouse_over_button = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rects[0].collidepoint(mouse_pos):
                        for i in P1_buttons:
                            button_selected[i] = False
                        button_selected[0] = True
                        self.P1sel = "coquinha"
                        self.sfx['coquinha'].play(0)
                    elif button_rects[5].collidepoint(mouse_pos):
                        for i in P2_buttons:
                            button_selected[i] = False
                        button_selected[5] = True
                        self.P2sel = "coquinha"
                        self.sfx['coquinha'].play(0)
                    elif button_rects[4].collidepoint(mouse_pos):
                        for i in P1_buttons:
                            button_selected[i] = False
                        button_selected[4] = True
                        self.P1sel = "calabresa"
                        self.sfx['calabresa'].play(0)
                    elif button_rects[1].collidepoint(mouse_pos):
                        for i in P2_buttons:
                            button_selected[i] = False
                        button_selected[1] = True
                        self.P2sel = "calabresa"
                        self.sfx['calabresa'].play(0)
                    elif button_rects[2].collidepoint(mouse_pos):
                        for i in P1_buttons:
                            button_selected[i] = False
                        button_selected[2] = True
                        self.P1sel = "farol"
                        self.sfx['farol'].play(0)
                    elif button_rects[7].collidepoint(mouse_pos):
                        for i in P2_buttons:
                            button_selected[i] = False
                        button_selected[7] = True
                        self.P2sel = "farol"
                        self.sfx['farol'].play(0)
                    elif button_rects[6].collidepoint(mouse_pos):
                        for i in P1_buttons:
                            button_selected[i] = False
                        button_selected[6] = True
                        self.P1sel = "rinha"
                        self.sfx['rinha'].play(0)
                    elif button_rects[3].collidepoint(mouse_pos):
                        for i in P2_buttons:
                            button_selected[i] = False
                        button_selected[3] = True
                        self.P2sel = "rinha"
                        self.sfx['rinha'].play(0)
            
            button_rects = self.draw_selection_buttons(screen)
            
            for i in range(len(button_selected)):
                if button_selected[i]:
                    pygame.draw.rect(screen, self.red, button_rects[i], 3)

            if self.P1sel != "" and self.P2sel != "":
                pygame.time.delay(3000)
                self.MapScreen(screen)
                running = False



            # Destacar botão quando o mouse está sobre ele
            if mouse_over_button:
                for rect in button_rects:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, self.green, rect, 3)
                        
            # Atualizar a tela
            pygame.display.flip()

    def TutorialScreen(self, screen):
        screen.fill(self.white)
        image_sel = pygame.image.load("imagens_tela_inicial/tela_tutorial.jpg")
        image_sel = pygame.transform.scale(image_sel, (self.width, self.height))
        image_sel_rect = image_sel.get_rect()
        screen.blit(image_sel, ((self.width - image_sel_rect.width) // 2, (self.height - image_sel_rect.height) // 2))
        pygame.display.flip()
        mouse_over_button = False
        button_rect = self.draw_tutorial_button(screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        mouse_over_button = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        self.InitialScreen(screen)
                        running= False

            button_rect = self.draw_tutorial_button(screen)

            # Destacar botão quando o mouse está sobre ele
            if mouse_over_button:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, self.green, button_rect, 3)

            # Atualizar a tela
            pygame.display.flip()
    
    def InitialScreen(self, screen):
        screen.fill(self.white)
        image_ini = pygame.image.load("imagens_tela_inicial/tela_de_inicio.jpg")
        image_ini = pygame.transform.scale(image_ini, (self.width, self.height))
        image_ini_rect = image_ini.get_rect()
        screen.blit(image_ini, ((self.width - image_ini_rect.width) // 2, (self.height - image_ini_rect.height) // 2))
        pygame.display.flip()
        mouse_over_button1 = False
        mouse_over_button2 = False
        running =  True
        button1_rect, button2_rect = self.draw_initial_buttons(screen)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_over_button1 = button1_rect.collidepoint(mouse_pos)
                    mouse_over_button2 = button2_rect.collidepoint(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_pos):
                        running = False
                        self.SelectionScreen(screen)
                    elif button2_rect.collidepoint(mouse_pos):
                        running = False
                        self.TutorialScreen(screen)
                        
            if not self.ready:
                button1_rect, button2_rect = self.draw_initial_buttons(screen)

                # Destacar botão quando o mouse está sobre ele
                if mouse_over_button1:
                    pygame.draw.rect(screen, self.green, button1_rect, 3)
                if mouse_over_button2:
                    pygame.draw.rect(screen, self.green, button2_rect, 3)

            # Atualizar a tela
            pygame.display.flip()
    
    def MapScreen(self, screen):
        screen.fill(self.white)
        image_ini = pygame.image.load("imagens_tela_inicial/tela_de_mapas.jpg")
        image_ini = pygame.transform.scale(image_ini, (self.width, self.height))
        image_ini_rect = image_ini.get_rect()
        screen.blit(image_ini, ((self.width - image_ini_rect.width) // 2, (self.height - image_ini_rect.height) // 2))
        pygame.display.flip()
        button1_rect, button2_rect, button3_rect, button4_rect, button5_rect = self.draw_map_buttons(screen)
        mouse_over_button1 = False
        mouse_over_button2 = False
        mouse_over_button3 = False
        mouse_over_button4 = False
        mouse_over_button5 = False
        button1_selected = False
        button2_selected = False
        button3_selected = False
        running =  True


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_over_button1 = button1_rect.collidepoint(mouse_pos)
                    mouse_over_button2 = button2_rect.collidepoint(mouse_pos)
                    mouse_over_button3 = button3_rect.collidepoint(mouse_pos)
                    mouse_over_button4 = button4_rect.collidepoint(mouse_pos)
                    mouse_over_button5 = button5_rect.collidepoint(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_pos):
                        self.map = "salaonegro"
                        button1_selected = True
                        button2_selected = False
                        button3_selected = False
                    elif button2_rect.collidepoint(mouse_pos):
                        self.map = "maromba"
                        button1_selected = False
                        button2_selected = True
                        button3_selected = False
                    elif button3_rect.collidepoint(mouse_pos):
                        self.map = "lago"
                        button1_selected = False
                        button2_selected = False
                        button3_selected = True
                    elif button4_rect.collidepoint(mouse_pos):
                        self.P1sel = ""
                        self.P2sel = ""
                        self.map = ""
                        self.SelectionScreen(screen)
                        running = False
                    elif button5_rect.collidepoint(mouse_pos):
                        if self.ready:
                            running = False
                        else:
                            print("Selecione uma mapa!")
                                   
            if self.map != "":
                self.ready = True
            
            button1_rect, button2_rect, button3_rect, button4_rect, button5_rect = self.draw_map_buttons(screen)

            if button1_selected:
                pygame.draw.rect(screen, self.red, button1_rect, 3)
            elif button2_selected:
                pygame.draw.rect(screen, self.red, button2_rect, 3)
            elif button3_selected:
                pygame.draw.rect(screen, self.red, button3_rect, 3)

            # Destacar botão quando o mouse está sobre ele
            if mouse_over_button1:
                pygame.draw.rect(screen, self.green, button1_rect, 3)
            elif mouse_over_button2:
                pygame.draw.rect(screen, self.green, button2_rect, 3)
            elif mouse_over_button3:
                pygame.draw.rect(screen, self.green, button3_rect, 3)
            elif mouse_over_button4:
                pygame.draw.rect(screen, self.green, button4_rect, 3)
            elif mouse_over_button5:
                pygame.draw.rect(screen, self.green, button5_rect, 3)

            # Atualizar a tela
            pygame.display.flip()
        pygame.display.flip()

    def EndScreen(self, screen, winner):
        self.P1sel = ""
        self.P2sel = ""
        self.map = ""
        screen.fill(self.white)
        image_fim = pygame.image.load("imagens_tela_inicial/P"+str(winner)+"_wins.jpg")
        image_fim = pygame.transform.scale(image_fim, (self.width, self.height))
        image_fim_rect = image_fim.get_rect()
        screen.blit(image_fim, ((self.width - image_fim_rect.width) // 2, (self.height - image_fim_rect.height) // 2))
        pygame.display.flip()
        mouse_over_button1 = False
        mouse_over_button2 = False
        running =  True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_over_button1 = button1_rect.collidepoint(mouse_pos)
                    mouse_over_button2 = button2_rect.collidepoint(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_pos):
                        self.play_again = True
                        running = False
                    elif button2_rect.collidepoint(mouse_pos):
                        running = False
                        

            button1_rect, button2_rect = self.draw_end_buttons(screen)

            # Destacar botão quando o mouse está sobre ele
            if mouse_over_button1:
                pygame.draw.rect(screen, self.green, button1_rect, 3)
            if mouse_over_button2:
                pygame.draw.rect(screen, self.green, button2_rect, 3)

            # Atualizar a tela
            pygame.display.flip()