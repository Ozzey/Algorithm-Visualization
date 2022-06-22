import pygame
from data import graph

# constants
display_width = 950
display_height = 600
radius = 30
speed = 3

#NODE AND EDGE COLORS
grey = (127,255,212)  # undiscovered edge
white = (255, 255, 255)  # discovered edge
yellow = (255,255,0)  # current node
red = (203,0,0)  # discovered node
black = (0, 0, 0)  # undiscovered node
blue = (0,0,255)  # completed node and completed edge

bg = pygame.image.load("assets/bg1.jpg")

def e_id(n1, n2): return tuple(sorted((n1, n2)))

class draw():
    def build_edges(self=None):
        global edges
        edges = {}
        for n1, (_, adjacents, _, _) in enumerate(graph):
            for n2 in adjacents:
                eid = e_id(n1, n2)
                if eid not in edges:
                    edges[eid] = [(n1, n2), grey]

    def draw_graph(self=None):
        global graph, window, edges

        for e in edges.values():
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
    queue = [0]
    window.blit(bg, (0, 0))
    pygame.display.flip()
    while len(queue) > 0:
        n1 = queue.pop(0)
        current = graph[n1]
        current[2] = white  # current color for node
        current[3] = yellow
        for n2 in current[1]:
            if graph[n2][3] == black and n2 not in queue:
                queue.append(n2)
                graph[n2][2] = white
                graph[n2][3] = red
                edges[e_id(n1, n2)][1] = white
                update()
        # Completed marked blue
        current[3] = blue
        update()

def update():
  global clock
  draw.draw_graph()
  pygame.display.update()
  clock.tick(speed)


def start():
    global window, edges, clock
    # add start colors to graph
    for element in graph:
      element.extend([grey, black])

    draw.build_edges()
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('BREADTH FIRST ALGORITHM')

    draw.draw_graph() # initial
    update()

    # Djikstra's Algorithm
    djikstra()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

start()