import pygame
from random import randint
import math
from sklearn.cluster import KMeans

pygame.init()

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
def create_text_render(string):
    return font.render(string, True, WHITE)

# func to calculate the distance of 2 points:
def distance(p1,p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1]-p2[1]) * (p1[1] - p2[1]))


screen = pygame.display.set_mode((1200,650))

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND_PANEL = (249 , 255, 230)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE =(255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)
CARAMEL = (133, 70, 30)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRASS, GRAPE, CARAMEL]

K = 0
error = 0
points = []
clusters = []
labels = []

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #Draw interface
    #Draw pane

    pygame.draw.rect(screen, BLACK, (50,50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    # K button +
    pygame.draw.rect(screen, BLACK, (850,50,50,50))
    screen.blit(create_text_render("+"), (850,50))

    # K button -
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    screen.blit(create_text_render("-"), (960, 50))

    # K value
    text_k = font.render('K = '+str(K), True, BLACK)
    screen.blit(text_k,(1050,50))

    # run button
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    screen.blit(create_text_render("Run"), (900,150))

    # random button
    pygame.draw.rect(screen, BLACK,(850, 250, 150, 50))
    screen.blit(create_text_render('Random'),(850,250))

    # Error value
    text_error = font.render('Error = '+str(error), True, BLACK)
    screen.blit(text_error,(850,350))

    # reset button
    pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
    screen.blit(create_text_render('Reset'), (850, 550))

    # Algorithm button scikit-learn
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit(create_text_render('Algorithm'), (850, 450))

    # draw mouse position when mouse is in panel

    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("("+str(mouse_x-50) +","+str(mouse_y-50)+")", True, BLACK)
        screen.blit(text_mouse,(mouse_x+10,mouse_y))

    #End draw interface


    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Create point on panel
            if 50< mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point =[mouse_x - 50, mouse_y - 50]
                points.append(point)


            # Change K button +
            if 850< mouse_x < 900 and 50 < mouse_y < 100:
                if K < 10:
                    K += 1
                    print("press K +")

            # Change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if K>0:
                    K-= 1
                print("press K -")

            # run button
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:

                # define the min distance of the point and clusters
                labels = []

                if clusters == []:
                    continue

                for point in points:
                    list_distances = []
                    for cluster in clusters:
                        list_distances.append(distance(cluster, point))
                        min_dist = min(list_distances)
                    labels.append(list_distances.index(min_dist))

                # update cluster point to the mean of each cluster
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    if count != 0:
                        clusters[i] = [sum_x/count, sum_y/count]

            # random button
            if 850 < mouse_x <1000 and 250 < mouse_y <300:
                clusters = []
                labels = []
                for i in range(K):
                    random_point = [randint(0, 700), randint(0, 500)]
                    clusters.append(random_point)
                print("random pressed")

            # reset button
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                points = []
                clusters = []
                labels = []
                error = 0

            # Algorithm button
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters=K).fit(points)
                labels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_

    # Draw cluster
    for i in range(len(clusters)):
            pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)

    # draw point circle
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0]+50, points[i][1]+50),6)
        if labels == []:
            pygame.draw.circle(screen, WHITE, (points[i][0]+50, points[i][1]+50), 5)
        else: # change data points color to the color of the nearest centroid
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 6)

    # calculate error
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
                error += round(distance(clusters[labels[i]], points[i]))

    pygame.display.flip()

pygame.quit()
