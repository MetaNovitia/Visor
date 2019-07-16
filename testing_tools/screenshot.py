import pyscreenshot as ImageGrab
from time import ctime,sleep
import sys

if __name__ == '__main__':
	t = 1
	i = 0
	if(len(sys.argv)>1): t=float(sys.argv[1])
	while True:
		# grab fullscreen
		im = ImageGrab.grab(bbox=(0, 30, 640, 340))

		# save image file
		im.save('T1/frame'+str(i)+'.png')

		i+=1
		print(ctime())
		sleep(t)
