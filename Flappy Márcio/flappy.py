import pygame
import os
import random


pygame.init()
# Inicializar o mixer de áudio
pygame.mixer.init()


# Carregar e reproduzir a música de fundo
pygame.mixer.music.load(os.path.join('music', 'flappymusic2.mp3'))
pygame.mixer.music.play(-1)  # Reproduzir em loop
som_de_morte = pygame.mixer.Sound(os.path.join('music', 'gameover.mp3'))  # som de morte


TELA_LARGURA = 500
TELA_ALTURA = 800
# CARREGAR AS IMAGENS ADICIONADAS
IMAGEM_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')),
                                          (TELA_LARGURA, TELA_ALTURA))
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_TELA_INICIAL = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'menu.png')),
                                            (TELA_LARGURA, TELA_ALTURA))
IMAGENS_PASSARO = [
   pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', '1.png'))),
   pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', '2.png'))),
   pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', '3.png'))),
]
IMAGENS_MARCIO = [
   pygame.transform.scale2x(pygame.image.load(os.path.join('marcioimg', f'frame-{str(i).zfill(2)}.gif')))
   for i in range(1, 31)
]
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)
FONTE_INICIO = pygame.font.SysFont('arial', 30)




class Passaro:
   IMGS = IMAGENS_PASSARO
   ROTACAO_MAXIMA = 25
   VELOCIDADE_ROTACAO = 20
   TEMPO_ANIMACAO = 5


   def __init__(self, x, y):
       self.x = 0
       self.y = y
       self.angulo = 0
       self.velocidade = 0
       self.altura = self.y
       self.tempo = 0
       self.contagem_imagem = 0
       self.imagem = self.IMGS[0]


   def pular(self):
       self.velocidade = -8
       self.tempo = 0
       self.altura = self.y


   def mover(self):
       self.tempo += 1
       deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo


       if deslocamento > 16:
           deslocamento = 16
       elif deslocamento < 0:
           deslocamento -= 2


       self.y += deslocamento


       if deslocamento < 0 or self.y < (self.altura + 50):
           if self.angulo < self.ROTACAO_MAXIMA:
               self.angulo = self.ROTACAO_MAXIMA
       else:
           if self.angulo > -90:
               self.angulo -= self.VELOCIDADE_ROTACAO


   def desenhar(self, tela):
       self.contagem_imagem += 1


       if self.contagem_imagem < self.TEMPO_ANIMACAO:
           self.imagem = self.IMGS[0]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
           self.imagem = self.IMGS[1]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
           self.imagem = self.IMGS[2]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
           self.imagem = self.IMGS[1]
       elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
           self.imagem = self.IMGS[0]
           self.contagem_imagem = 0


       if self.angulo <= -80:
           self.imagem = self.IMGS[1]
           self.contagem_imagem = self.TEMPO_ANIMACAO * 2


       imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
       pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
       retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
       tela.blit(imagem_rotacionada, retangulo.topleft)


   def get_mask(self):
       return pygame.mask.from_surface(self.imagem)




class Cano:
   DISTANCIA = 200
   VELOCIDADE = 5


   def __init__(self, x):
       self.x = x
       self.altura = 0
       self.pos_topo = 0
       self.pos_base = 0
       self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
       self.CANO_BASE = IMAGEM_CANO
       self.passou = False
       self.definir_altura()


   def definir_altura(self):
       self.altura = random.randrange(50, 450)
       self.pos_topo = self.altura - self.CANO_TOPO.get_height()
       self.pos_base = self.altura + self.DISTANCIA


   def mover(self):
       self.x -= self.VELOCIDADE


   def desenhar(self, tela):
       tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
       tela.blit(self.CANO_BASE, (self.x, self.pos_base))


   def colidir(self, passaro):
       passaro_mask = passaro.get_mask()
       topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
       base_mask = pygame.mask.from_surface(self.CANO_BASE)


       distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
       distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))


       topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
       base_ponto = passaro_mask.overlap(base_mask, distancia_base)


       return base_ponto or topo_ponto




class Chao:
   VELOCIDADE = 5
   LARGURA = IMAGEM_CHAO.get_width()
   IMAGEM = IMAGEM_CHAO


   def __init__(self, y):
       self.y = y
       self.x1 = 0
       self.x2 = self.LARGURA


   def mover(self):
       self.x1 -= self.VELOCIDADE
       self.x2 -= self.VELOCIDADE


       if self.x1 + self.LARGURA < 0:
           self.x1 = self.x2 + self.LARGURA
       if self.x2 + self.LARGURA < 0:
           self.x2 = self.x1 + self.LARGURA


   def desenhar(self, tela):
       tela.blit(self.IMAGEM, (self.x1, self.y))
       tela.blit(self.IMAGEM, (self.x2, self.y))




def desenhar_tela_inicial(tela):
   tela.blit(IMAGEM_TELA_INICIAL, (0, 0))




def desenhar_tela(tela, passaros, canos, chao, pontos, perdeu, tela_inicial):
   if tela_inicial:
       desenhar_tela_inicial(tela)
   else:
       tela.blit(IMAGEM_BACKGROUND, (0, 0))
       for passaro in passaros:
           passaro.desenhar(tela)
       for cano in canos:
           cano.desenhar(tela)


       texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
       tela.blit(texto_pontos, (TELA_LARGURA - 10 - texto_pontos.get_width(), 10))
       chao.desenhar(tela)


   if perdeu:
       # Exibe as imagens do GIF sequencialmente
       for imagem_marcio in IMAGENS_MARCIO:
           largura_da_imagem = imagem_marcio.get_width()
           altura_da_imagem = imagem_marcio.get_height()
           x = (TELA_LARGURA - largura_da_imagem) / 2
           y = (TELA_ALTURA - altura_da_imagem) / 2
           tela.blit(imagem_marcio, (x, y))
           pygame.display.update()
           pygame.time.delay(100)
   if not tela_inicial:
       texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
       tela.blit(texto_pontos, (TELA_LARGURA - 10 - texto_pontos.get_width(), 10))
   chao.desenhar(tela)




def reiniciar_jogo():
   passaros = [Passaro(230, 350)]
   chao = Chao(730)
   canos = [Cano(700)]
   pontos = 0
   perdeu = False


   # Parar a reprodução do som de "game over"
   som_de_morte.stop()


   return passaros, chao, canos, pontos, perdeu




def main():
   tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
   pygame.display.set_caption("Flappy Bird")


   passaros = [Passaro(230, 350)]
   chao = Chao(730)
   canos = [Cano(700)]
   pontos = 0
   perdeu = False
   tela_inicial = True
   iniciado = False
   som_de_morte_tocado = False


   # Reiniciar a música ao recomeçar o jogo
   pygame.mixer.music.load(os.path.join('music', 'flappymusic2.mp3'))
   pygame.mixer.music.play(-1)
   clock = pygame.time.Clock()


   rodando = True


   while rodando:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               rodando = False
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   if tela_inicial:
                       tela_inicial = False
                       iniciado = True
                   elif not perdeu:
                       for passaro in passaros:
                           passaro.pular()
                   elif perdeu:
                       # Reiniciar o jogo se perder
                       passaros, chao, canos, pontos, perdeu = reiniciar_jogo()
                       tela_inicial = True
                       iniciado = False
                       # Reiniciar a música de fundo
                       pygame.mixer.music.load(os.path.join('music', 'flappymusic2.mp3'))
                       pygame.mixer.music.play(-1)


       if iniciado:
           # Lógica do jogo quando estiver iniciado
           for passaro in passaros:
               passaro.mover()
           chao.mover()


           adicionar_cano = False
           remover_canos = []
           for cano in canos:
               for i, passaro in enumerate(passaros):
                   if cano.colidir(passaro):
                       passaros.pop(i)
                       perdeu = True
                       pygame.mixer.music.stop()  # Parar a música de fundo
                       som_de_morte.play()  # Reproduzir o som de morte
                       break
                   if not cano.passou and passaro.x > cano.x:
                       cano.passou = True
                       adicionar_cano = True
               cano.mover()
               if cano.x + cano.CANO_TOPO.get_width() < 0:
                   remover_canos.append(cano)


           if adicionar_cano:
               pontos += 1
               canos.append(Cano(600))
           for cano in remover_canos:
               canos.remove(cano)


           if not perdeu:
               for i, passaro in enumerate(passaros):
                   if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                       passaros.pop(i)
                       perdeu = True
                       pygame.mixer.music.stop()  # Parar a música de fundo
                       som_de_morte.play()  # Reproduzir o som de morte


       desenhar_tela(tela, passaros, canos, chao, pontos, perdeu, tela_inicial)
       pygame.display.update()
       clock.tick(30)


   pygame.quit()




if __name__ == '__main__':
   main()

