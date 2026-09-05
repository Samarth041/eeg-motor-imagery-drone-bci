import pygame

#====================================================
#Configuration
#===================================================

SCREEN_WIDTH=900
SCREEN_HEIGHT=600

DRONE_SIZE=40
DRONE_SPEED=250

#==========================================================
#DRONE
#==========================================================


class Drone:
    def __init__(self,x,y):
        self.x=float(x)
        self.y=float(y)

        self.command="HOVER"

    def update(self,dt):
        if self.command=="LEFT":
            self.x-=DRONE_SPEED*dt

        elif self.command=="RIGHT":
            self.x+=DRONE_SPEED*dt

        elif self.command=="UP":
            self.y-=DRONE_SPEED*dt

        elif self.command=="DOWN":
            self.x+=DRONE_SPEED*dt

        #keep drone inside screen

        self.x=max(
            DRONE_SIZE,
            min(SCREEN_WIDTH-DRONE_SIZE,self.x),
        )

        self.y=max(
            DRONE_SIZE,
            min(SCREEN_HEIGHT-DRONE_SIZE,self.y)
        )

    def draw(self,screen):
        #Draw a simple drone body

        pygame.draw.rect(
            screen,
            (70,130,220),
            (
                int(self.x-20),
                int(self.y-10),
                40,
                20
            ),
        )

        #draw two rotors

        pygame.draw.circle(
            screen,
            (40,40,40),
            (int(self.x-25),int(self.y)),
            8
        )

        pygame.draw.circle(
            screen,
            (40,40,40),
            (int(self.x+25),int(self.y))
        )

#===================================================================
#Main
#==================================================================

def main():
    pygame.init()

    screen=pygame.display.set_mode(
        (SCREEN_WIDTH,SCREEN_HEIGHT)
    )

    pygame.display.set_caption(
        "EEG DRONE BCI-SIMULATOR"
    )

    drone=DRONE(
        SCREEN_WIDTH//2,
        SCREEN_HEIGHT//2
    )

    running=True

    while running:
        dt=clock.tick(60)/1000.0

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running=False

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    drone.set_command("LEFT")

                elif event.key==pygame.K_RIGHT:
                    drone.set_commaq("RIGHT")

                elif event.key==pygame.K_UP:
                    drone.set_commaq("UP")


                elif event.key==pygame.K_DOWN:
                    drone.set_commaq("DOWN")

                elif event.key==pygame.K_SPACE:
                    drone.set_commaq("HOVER")

        drone.update(dt)

        screen.fill((235,240,245))

        drone.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()

