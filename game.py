import asyncio
from components import Stick, Ring, ScreenManager
import pygame

async def solve(manager: ScreenManager, stick: Stick, n):
    if manager.status.pause:
        return 
    if n == 0:
        manager.status.step += manager.status.sign
        if stick[0].on_stick:
            await stick[0].move_down(manager)
        else:
            await stick[0].move_up(manager)
        return 
    
    if not stick[n-1].on_stick:
        await solve(manager, stick, n-1)
    
    for i in range(n-2, -1, -1):
        if stick[i].on_stick:
            await solve(manager, stick, i)
    
    if stick[n].on_stick:
        await stick[n].move_down(manager)
    else:
        await stick[n].move_up(manager)

    manager.status.step += manager.status.sign
    manager.update()


async def main():
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    stick = Stick(300, 250)
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
            manager.status.pause = False
        # If the right mouse button is pressed and the mouse is over the ring
        elif mouse_pressed[2]:
            manager.status.pause = True
        
        for i in range(8, 0, -1):
            async with asyncio.Lock() as lock:
                await solve(manager, stick, i)
                await asyncio.sleep(0.1)

        # Update and draw the screen
        manager.update()

asyncio.run(main())

# Quit pygame
pygame.quit()
