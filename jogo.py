#Importando bibliotecas
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


# Função para desenhar formas geométricas com cores
def draw_shape(vertices, color):
    glColor3f(*color)   #definindo a cor dos vértices
    glBegin(GL_POLYGON)
    for vertex in vertices:     #itera sobre os vétices 
        glVertex2f(vertex[0], vertex[1])        #define cada vértice do polígono x e y
    glEnd() # finaliza a definição
    
    

# Funções para criar diferentes formas geométricas
def create_circle(radius, num_segments):  #criando um círculo
    return [(np.cos(2 * np.pi * i / num_segments) * radius, np.sin(2 * np.pi * i / num_segments) * radius) for i in range(num_segments)]

def create_square(size):    #criando um quadado
    return [(-size, -size), (size, -size), (size, size), (-size, size)]

def create_triangle(size):      #criando um triângulo equilátero
    return [(-size, -size), (size, -size), (0, size)]

def create_pentagon(size):      #criando um pentagono
    return [(np.cos(2 * np.pi * i / 5) * size, np.sin(2 * np.pi * i / 5) * size) for i in range(5)]

# Função para verificar se o ponto está dentro do polígono
def is_point_inside_polygon(point, vertices):
    x, y = point            # Coordenadas do ponto
    n = len(vertices)       # Número de vértices do polígono
    inside = False          # Flag para indicar se o ponto está dentro do polígono
    p1x, p1y = vertices[0]  # Primeiro vértice do polígono
    for i in range(n + 1):  # Itera sobre todos os vértices do polígono
        p2x, p2y = vertices[i % n]  # Próximo vértice do polígono
        if y > min(p1y, p2y): # Se o ponto estiver acima do segmento de reta definido pelos vértices
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x  # Calcula a interseção
                    if p1x == p2x or x <= xinters:
                        inside = not inside     # Inverte o estado da flag
        p1x, p1y = p2x, p2y  # Move para o próximo vértice   
    return inside           # Retorna se o ponto está dentro do polígono ou não

# Inicialização do ambiente
def main():
    "Função principal do meu programa"
    pygame.init()  # inicializando o Pygame
    display = (800, 600)  # Tamanho da janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL) #modo da minha janela
    gluOrtho2D(-400, 400, -300, 300)  # definindo a pojeção

    
        #Criando lista e definindo vértices e cores específicas
    shapes = [ 
        {'vertices': create_circle(50, 32), 'color': (1, 0.5, 0.5)},  # Círculo - Rosa
        {'vertices': create_square(50), 'color': (1, 0.647, 0)},      # Quadrado - Laranja
        {'vertices': create_triangle(50), 'color': (1, 1, 0)},        # Triângulo - Amarelo
        {'vertices': create_pentagon(50), 'color': (0.529, 0.808, 0.98)}  # Pentágono - Azul
    ]

    #Posições onde as formas serão desenhadas e suas cores.
    destinations = [
        {'position': [-200, 200], 'color': (0.5, 0.5, 0.5)},
        {'position': [0, 200], 'color': (0.5, 0.5, 0.5)},
        {'position': [200, 200], 'color': (0.5, 0.5, 0.5)},
        {'position': [0, 0], 'color': (0.5, 0.5, 0.5)}
    ]

    # Posição e transformação inicial das formas
    objects = [
        {'vertices': shapes[i]['vertices'], 'position': [i * 100 - 150, -200], 'scale': 1, 'rotation': 0, 'color': shapes[i]['color']} for i in range(len(shapes))
    ]

    selected_object = None       # Objeto selecionado (inicialmente nenhum)
    running = True      # Variável para controlar a execução do programa
    while running:
        for event in pygame.event.get(): # Captura eventos do Pygame
            if event.type == pygame.QUIT:
                running = False          # Finaliza o loop principal
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se o evento for um clique do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()   # Obtém a posição do mouse
                
                # Converter coordenadas do mouse para o sistema de coordenadas do OpenGL
                mouse_x = (mouse_x - display[0] / 2) * (800 / display[0])
                mouse_y = -(mouse_y - display[1] / 2) * (600 / display[1])
                for obj in objects: # Itera sobre os objetos
                    
                    transformed_vertices = [(v[0] * obj['scale'], v[1] * obj['scale']) for v in obj['vertices']]
                    if is_point_inside_polygon((mouse_x - obj['position'][0], mouse_y - obj['position'][1]),  transformed_vertices):        # Verifica se o clique do mouse está dentro do objeto
                        selected_object = obj
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_object = None


        keys = pygame.key.get_pressed()     # Obtém o estado das teclas pressionadas
        if selected_object:                 # Se houver um objeto selecionado
            if keys[pygame.K_UP]:
                selected_object['position'][1] += 1 #Move para cima
            if keys[pygame.K_DOWN]:                 #Move paa baixo
                selected_object['position'][1] -= 1  
            if keys[pygame.K_LEFT]:
                selected_object['position'][0] -= 1
            if keys[pygame.K_RIGHT]:
                selected_object['position'][0] += 1
            if keys[pygame.K_a]:                    # Rotaciona o objeto no sentido anti-horário
                selected_object['rotation'] += 1    
            if keys[pygame.K_d]:                    # Rotaciona o objeto no sentido horário
                selected_object['rotation'] -= 1
            if keys[pygame.K_w]:                    # Aumenta a escala do objeto
                selected_object['scale'] += 0.01
            if keys[pygame.K_s]:    # Se a tecla "S" estiver pressionada diminui a escala do objeto
                selected_object['scale'] -= 0.01

        if selected_object:     # Se houver um objeto selecionado
            mouse_x, mouse_y = pygame.mouse.get_pos()       # Obtém a posição do mouse
            mouse_x = (mouse_x - display[0] / 2) * (800 / display[0])     # Converte a posição do mouse para o sistema de coordenadas OpenGL
            mouse_y = -(mouse_y - display[1] / 2) * (600 / display[1])
            selected_object['position'] = [mouse_x, mouse_y]               # Define a nova posição do objeto como a posição do mouse

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)      # Limpa o buffer de cor e de profundidade

        # Desenhar destinos
        for i, dest in enumerate(destinations):
            glPushMatrix()  # Empurra a matriz atual para a pilha de matriz
            glTranslatef(dest['position'][0], dest['position'][1], 0)       # Translada para a posição do destino
            draw_shape(shapes[i]['vertices'], dest['color'])                # Desenha a forma do destino
            glPopMatrix()       # Puxa a matriz da pilha de matriz

        # Desenhar formas
        for obj in objects:  # Itera sobre os objetos
            glPushMatrix()     # Empurra a matriz atual para a pilha de matriz
            glTranslatef(obj['position'][0], obj['position'][1], 0)      # Translada para a posição do objeto
            glRotatef(obj['rotation'], 0, 0, 1)     # Rotaciona o objeto
            glScalef(obj['scale'], obj['scale'], 1)     # Escala o objeto
            draw_shape(obj['vertices'], obj['color'])   # Desenha a forma do objeto
            glPopMatrix()   # Puxa a matriz da pilha de matriz


        pygame.display.flip()   # Atualiza a tela
        pygame.time.wait(10)    # Espera um pouco antes de atualizar novamente

    pygame.quit()   # Sai do Pygame

if __name__ == "__main__":      # Chama a função principal se este arquivo for executado diretamente
    main()