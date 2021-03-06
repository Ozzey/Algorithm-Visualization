import pygame
from data import graph
import button

# constants
width = 950
height = 610
size = 30
speed = 3
#NODE AND EDGE COLORS
grey = (127,255,212)  # undiscovered edge
white = (255, 255, 255)  # discovered edge
yellow = (255,255,0)  # live node
red = (203,0,0)  # discovered node
black = (0, 0, 0)  # undiscovered node
blue = (0,0,255)  # completed node and completed edge

bg = pygame.image.load("assets/bg1.jpg")

def e_id(n1, n2): return tuple(sorted((n1, n2)))

game_over = False

#load button images
pg = pygame.image.load('assets/exit.png')
start_img = pygame.transform.scale(pg, (120, 90))
start_button = button.Button(720, 250, start_img, 0.8)

def game_over():
    global game_over
    game_over = True

class draw():
    def build_edj(self=None):
        global edj
        edj = {}
        for n1, (_, adj, _, _) in enumerate(graph):
            for n2 in adj:
                eid = e_id(n1, n2)
                if eid not in edj:
                    edj[eid] = [(n1, n2), grey]

    def draw_graph(self=None):
        global graph, window, edj

        for e in edj.values():
            (n1, n2), color = e
            pygame.draw.line(window, color, graph[n1][0], graph[n2][0], 2)
        for xy, _, lcolor, fcolor in graph:
            draw.fill(xy, lcolor, fcolor, 25, 2)


    def fill(xy, line_color, fill_color, radius, thickness):
        global window
        pygame.draw.circle(window, line_color, xy, radius)
        pygame.draw.circle(window, fill_color, xy, radius - thickness)


#Djikstra Algorithm Implementation
def djikstra():
    nodes = [0]
    window.blit(bg, (0, 0))
    pygame.display.flip()
    run = True
    while len(nodes) > 0 and run:
        if start_button.draw(window):
            run = False
        n1 = nodes.pop(0)
        live = graph[n1]
        live[2] = white  # live color for node
        live[3] = yellow
        for n2 in live[1]:
            if graph[n2][3] == black and n2 not in nodes:
                nodes.append(n2)
                graph[n2][2] = white
                graph[n2][3] = red
                edj[e_id(n1, n2)][1] = white
                update()
        # Completed marked blue
        live[3] = blue
        update()

def update():
  draw.draw_graph()
  pygame.display.update()
  clock.tick(speed)

def start():
    pygame.init()
    global window, edj, clock
    # add start colors to graph
    for element in graph:
      element.extend([grey, black])
    draw.build_edj()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((width, height),pygame.NOFRAME)
    pygame.display.set_caption("DJIKSTRA'S ALGORITHM")
    draw.draw_graph() # initial
    update()
    # Djikstra's Algorithm
    djikstra()
    running = True
    while running:
        for event in pygame.event.get():
            if start_button.draw(window):
                pygame.time.delay(500)
                running = False
            if event.type == pygame.QUIT:
                running = False
        if running:
            pygame.display.update()

start()
