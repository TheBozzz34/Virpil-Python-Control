import pygame
from time import sleep
from djitellopy import Tello
import tkinter as tk

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

tello = Tello()


tello.connect()


root = tk.Tk()
root.title("Tello Virpil Control")

x_label = tk.Label(root, text="X Axis:")
x_label.pack()
y_label = tk.Label(root, text="Y Axis:")
y_label.pack()


def map_joystick_to_tello(x, y):
    speed = int(x * 100)
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
        x_axis = joystick.get_axis(1)
        y_axis = joystick.get_axis(0)
        

        x_label.config(text=f"X Axis: {x_axis:.2f}")
        y_label.config(text=f"Y Axis: {y_axis:.2f}")
        

        map_joystick_to_tello(x_axis, y_axis)
        

        sleep(0.05)

except KeyboardInterrupt:
    tello.send_rc_control(0, 0, 0, 0)
    tello.land()
    tello.end()

    root.destroy()
