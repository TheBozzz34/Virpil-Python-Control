import pygame
from time import sleep
from djitellopy import Tello
import tkinter as tk

# Joystick Initilization Code
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Tello Initilization Code
tello = Tello()
tello.connect()


# GUI Code (Not Working)
root = tk.Tk()
root.title("Tello Virpil Control")

x_label = tk.Label(root, text="X Axis:")
x_label.pack()
y_label = tk.Label(root, text="Y Axis:")
y_label.pack()


# Send RC Control to Tello, no response needed
def map_joystick_to_tello(x, y):
    speed = int(-x * 100)
    turn = int(y * 100)
    

    if abs(speed) < 10:
        speed = 0
    if abs(turn) < 10:
        turn = 0
    
    tello.send_rc_control(0, speed, 0, turn)

try:
    while True:
        pygame.event.pump()
        
        # Flip cause virpil joystick is funky
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        

        x_label.config(text=f"X Axis: {x_axis:.2f}")
        y_label.config(text=f"Y Axis: {y_axis:.2f}")
        

        map_joystick_to_tello(x_axis, y_axis)

        # Individual Button Mapping
        if (joystick.get_button(3) == 1):
            tello.land()
        if (joystick.get_button(9) == 1 ):
            tello.takeoff()
        if (joystick.get_button(17) == 1):
            tello.move_up(30)
        if (joystick.get_button(18) == 1):
            tello.move_down(30)

        sleep(0.05)

except KeyboardInterrupt:
    tello.send_rc_control(0, 0, 0, 0)
    tello.land()
    tello.end()

    root.destroy()
