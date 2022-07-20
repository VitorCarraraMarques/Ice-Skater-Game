import pygame, sys
#sys.path.append(".")
#from ice_skater_class import Ice_Skater

pygame.init()

width = 1528
height = 800
size = width, height 
screen = pygame.display.set_mode(size)
 
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "Background1.png")), (width, height)
)

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 20, 20)
blue = (20, 20, 200)
yellow = (150, 150, 0)
bright_blue = (100, 100, 200)

FPS = 60
clock = pygame.time.Clock()


def soma_vetor2D(A, B): 
    return [A[0] + B[0], A[1] + B[1]]



class Ice_Skater:

    def __init__(self):
        self.width = 30 
        self.pos = [100, 470]
        self.vel = [0, 0]
        self.mod_vel = 50*(self.vel[0]**2 + self.vel[1]**2)
        self.acc = [0, 0]
        self.mass = 5
        self.skater_rect = pygame.Rect(self.pos[0] - self.width, self.pos[1] - self.width, self.width*2, self.width*2)

    def move(self):
        self.vel = soma_vetor2D(self.vel, self.acc) 
        self.pos = soma_vetor2D(self.pos, self.vel) 

    def force_right_or_left(self):
        force = [0, 0]
        
        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            force = [0.5, 0]

        elif pygame.key.get_pressed()[pygame.K_LEFT] == True:
            force = [-0.5, 0]

        return force

    def jump(self): 
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] == True and (
           (self.skater_rect.colliderect(obstacle) and self.skater_rect.bottom - obstacle.top < 30) or (self.pos[1] > 760)):
            self.vel[1] = -8
    
    def gravity(self): 
        grav_const = [0, 0.08]
        force = [self.mass*grav_const[0], self.mass*grav_const[1]]
        return force  

    def get_acc(self, force):
        acc = [0, 0]
        acc[0] = force[0]/self.mass
        acc[1] = force[1]/self.mass
        return acc 
    
    def add_acc(self, acc): 
        self.acc[0] += acc[0]
        self.acc[1] += acc[1]

    def reset_acc(self):
        self.acc = [0, 0]


    def edges(self):
        loss = 0.5
        if self.pos[0] < self.width :
            self.pos[0] = self.width
            self.vel[0] = -loss*self.vel[0]
            
        elif self.pos[0] > width - self.width:    
            self.pos[0] = width - self.width
            self.vel[0] = -loss*self.vel[0]
            
        elif self.pos[1] < self.width:
            self.pos[1] = self.width
            self.vel[1] = -loss*self.vel[1]

        elif self.pos[1] > height - (self.width):
            self.pos[1] = height - (self.width)
            self.vel[1] = -loss*self.vel[1] 
        

    def show(self):    
        #ice_skater_img = pygame.image.load('@coisas\projetos python\Visual Studio Code Projects\Untitled Ice Skater Game\IceSkater.png')
        #ice_skater_img = pygame.image.load('IceSkater.png')
        self.skater_rect = pygame.Rect(self.pos[0] - self.width, self.pos[1] - self.width, self.width*2, self.width*2) 
        #pygame.draw.rect(screen, blue, ice_skater_img)



class Obstacle: 
    def __init__(self, left, top, width, height): 
        self.obstacle_rect = pygame.Rect(left, top, width, height)
        self.bigger = 20
        self.bigger_rect = pygame.Rect(left - self.bigger, top - self.bigger, width + 2*self.bigger, height + 2*self.bigger)

    def show(self): 
        pygame.draw.rect(screen, (150, 150, 200), self.bigger_rect)
        pygame.draw.rect(screen, (40, 40, 120), self.obstacle_rect)



def collision(body, obstacle): 
    loss = 0.2
    #COLISÃO POR CIMA
    if ((obstacle.point_1[0] <= body.pos[0] <= obstacle.point_2[0]) and (obstacle.point_1[1] <= body.pos[1] + body.width <= obstacle.point_1[1] + 100)):
        #body.vel[1] = - loss*body.vel[1]
        body.vel[1] = 0
    #COLISÃO POR BAIXO
    elif ((obstacle.point_1[0] <= body.pos[0] <= obstacle.point_2[0]) and (obstacle.point_3[1] - 100 <= body.pos[1] - body.width <= obstacle.point_3[1] )):
        #body.vel[1] = - loss*body.vel[1]
        body.vel[1] = 0
    #COLISÃO PELA DIREITA
    elif ((obstacle.point_2[0] - 100 <= body.pos[0] - body.width <= obstacle.point_2[0]) and (obstacle.point_2[1] <= body.pos[1] <= obstacle.point_3[1])):
        #body.vel[0] = - loss*body.vel[0]
        body.vel[0] = 0
    #COLISÃO PELA ESQUERDA
    elif ((obstacle.point_1[0] <= body.pos[0] + body.width <= obstacle.point_1[0] + 100) and (obstacle.point_2[1] <= body.pos[1] <= obstacle.point_3[1])):
        #body.vel[0] = - loss*body.vel[0]
        body.vel[0] = 0
    return True
        


ice_skater = Ice_Skater()

obstacle_1 = Obstacle((0, 500),(550, 500),(550, 700),(0, 700))
obstacle_0 = Obstacle((650, 200), (850, 200), (850, 400), (650, 400)) 
obstacle_2 = Obstacle((800, 650), (1500, 650), (1500, 800), (800, 800))
obstacles_list = []
obstacles_list.append(obstacle_0)
obstacles_list.append(obstacle_1)
obstacles_list.append(obstacle_2)



while True: 
    clock.tick(FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(black)

    for i in range(len(obstacles_list)):
        obstacles_list[i].show()

    ice_skater.show()
    ice_skater.move()
    ice_skater.reset_acc()
    #ice_skater.jump()

    
    key_force = ice_skater.force_right_or_left()
    acc_key = ice_skater.get_acc(key_force)
    ice_skater.add_acc(acc_key)
    

    ice_skater.edges()

    gravit_force = ice_skater.gravity()
    acc_grav = ice_skater.get_acc(gravit_force)
    ice_skater.add_acc(acc_grav)
    
    for i in range(len(obstacles_list)): 
        collision(ice_skater, obstacles_list[i])

    ice_skater.jump()
    
    pygame.display.flip()