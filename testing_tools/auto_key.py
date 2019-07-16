import pyautogui
import time
from pynput.mouse import Controller
from random import seed,random,randint

movement = ["left","right"]

seed(0)

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

(w,h) = pyautogui.size()
mouse = Controller()
time.sleep(7)

"""pyautogui.press('esc')
pyautogui.moveTo(w/2,20)
for i in range(10):
    pyautogui.move(-10,0)"""

#mouse.position = (0,h/2)

pyautogui.keyDown('w')

while(mouse.position[0]<640):
    time.sleep(randint(1,10))
    key = movement[randint(0,1)]
    pyautogui.keyDown(key)
    time.sleep(random()/10)
    pyautogui.keyUp(key)

pyautogui.keyUp('w')
