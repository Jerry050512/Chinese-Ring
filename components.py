# A pygame program to demonstrate the Chinese ring puzzle
from colors import *
import pygame
import asyncio

# Initialize pygame
pygame.init()

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RING_WIDTH = 10
RING_HEIGHT = 160
RING_COLOR = (255, 192, 203) # Pink
STICK_WIDTH = 600
STICK_HEIGHT = 15
FPS = 60 # Frames per second
DELAY = 0.01 # Time delay in seconds

# Create a screen object and set the title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Demo")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Define a class to represent the ring as a sprite
class Ring(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0) -> None:
        # Call the parent class constructor
        super().__init__()
        # Create a surface for the ring and fill it with the ring color
        self.image = pygame.Surface((RING_WIDTH, RING_HEIGHT))
        self.image.fill(RING_COLOR)
        # Get the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Set the initial position of the rectangle
        self.rect.x = x
        self.rect.y = y
        # Set a flag to indicate if the ring is on the stick
        self.on_stick = True
    
    # Define a method to move the ring up or down by a given distance
    async def move(self, manager, distance=50):
        # If the distance is zero, do nothing
        if distance == 0:
            return
        # Get the sign of the distance
        sign = int(distance / abs(distance))
        # Loop from zero to the absolute value of the distance
        for i in range(0, abs(distance)):
            # Move the rectangle by the sign value in the y direction
            self.rect.move_ip(0, sign)
            manager.update()
            # Wait for the time delay
            await asyncio.sleep(DELAY)

    async def move_down(self, manager, distance=50):
        if not self.on_stick:
            return 
        self.on_stick = False
        await self.move(manager, distance)
    
    async def move_up(self, manager, distance=50):
        if self.on_stick:
            return 
        self.on_stick = True
        await self.move(manager, -distance)
    
    # Define a method to resize the ring by a given factor
    def resize(self, factor):
        # Get the new width and height by multiplying the current values by the factor
        new_width = int(self.rect.width * factor)
        new_height = int(self.rect.height * factor)
        # Scale the image to the new size
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        # Get the new rectangle object
        self.rect = self.image.get_rect()
    
    # Define a method to rotate the ring by a given angle
    def rotate(self, angle):
        # Rotate the image by the angle
        self.image = pygame.transform.rotate(self.image, angle)
        # Get the new rectangle object
        self.rect = self.image.get_rect()

# Define a class to represent the ring as a sprite
class Stick(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, ring_num=9) -> None:
        # Call the parent class constructor
        super().__init__()
        # Create a surface for the ring and fill it with the ring color
        self.image = pygame.Surface((STICK_WIDTH, STICK_HEIGHT))
        self.image.fill(WHITE)
        # Get the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Set the initial position of the rectangle
        self.rect.x = x
        self.rect.y = y

        self.rings = [Ring(x+i*3*RING_WIDTH, y) for i in range(ring_num)]
        self.first_on_ring = self.rings[0] 

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.rings[index]
        if isinstance(index, slice):
            start = index.start or 0 # 如果沒有指定，則默認為 0
            stop = index.stop or len(self.lst) # 如果沒有指定，則默認為序列長度
            step = index.step or 1 # 如果沒有指定，則默認為 1
            # 根據切片的參數，返回一個新的列表
            return [self.rings[i] for i in range(start, stop, step)]
        # 如果 index 是其他類型，則拋出異常
        else:
            raise TypeError("index must be int or slice")
    
    # Define a method to move the ring up or down by a given distance
    async def move(self, manager, distance=50):
        # If the distance is zero, do nothing
        if distance == 0:
            return
        # Get the sign of the distance
        sign = int(distance / abs(distance))
        # Loop from zero to the absolute value of the distance
        for i in range(0, abs(distance)):
            # Move the rectangle by the sign value in the y direction
            self.rect.move_ip(sign, 0)
            manager.update()
            # Wait for the time delay
            await asyncio.sleep(DELAY)
    
    # Define a method to resize the ring by a given factor
    def resize(self, factor):
        # Get the new width and height by multiplying the current values by the factor
        new_width = int(self.rect.width * factor)
        new_height = int(self.rect.height * factor)
        # Scale the image to the new size
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        # Get the new rectangle object
        self.rect = self.image.get_rect()
    
    # Define a method to rotate the ring by a given angle
    def rotate(self, angle):
        # Rotate the image by the angle
        self.image = pygame.transform.rotate(self.image, angle)
        # Get the new rectangle object
        self.rect = self.image.get_rect()

class Status:
    def __init__(self) -> None:
        self.pause = True
        self.step = 0
        self.sign = 1

# Define a class to manage the screen and the sprites
class ScreenManager:
    def __init__(self, screen: pygame.Surface, *args) -> None:
        # Store the screen object
        self.screen = screen
        # Create a sprite group and add the sprites
        self.sprites = pygame.sprite.Group()
        self.sprites.add(*args)

        self.status = Status()
    
    def add(self, *args):
        self.sprites.add(*args)
    
    # Define a method to update and draw the sprites on the screen
    def update(self):
        # Fill the screen with black
        self.screen.fill((0, 0, 0))
        # Update the sprites
        self.sprites.update()
        # Draw the sprites
        self.sprites.draw(self.screen)
        # Update the display
        pygame.display.flip()

if __name__ == '__main__':
    # Create a ring object and set its position
    # ring = Ring(400, 100)
    stick = Stick(300, 250)
    # Create a screen manager object and add the ring
    manager = ScreenManager(screen, stick, *stick.rings)

    # Enter the main loop
    running = True
    while running:
        # Handle the events
        for event in pygame.event.get():
            # If the user clicks the close button, exit the program
            if event.type == pygame.QUIT:
                running = False
            # If the user resizes the window, adjust the screen size
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) 
        
        # Get the mouse button state and position
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # If the left mouse button is pressed and the mouse is over the ring
        if mouse_pressed[0]:
            # Resize the ring by a factor of 1.1
            asyncio.run(stick.move(manager, 50))
        # If the right mouse button is pressed and the mouse is over the ring
        elif mouse_pressed[2]:
            # Rotate the ring by 10 degrees
            asyncio.run(stick.move(manager, -50))
        
        # Update and draw the screen
        manager.update()
        # Control the frame rate
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
