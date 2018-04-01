import RPi.GPIO as GPIO
from time import sleep
from subprocess import Popen, PIPE
import threading

#GPIO Ports
Enc_A = 5
Enc_B = 13
Enc_P = 12
But_B = 17

#define buttons to be pressed
r = 'key Down' 		#changed right/left to up/down because of new list format
l = 'key Up' 		#changed right/left to up/down because of new list format
e = 'key Return'
u = 'key Up'
d = 'key Down'
back = 'key BackSpace'
c = 'key c'

#initialize pdf status
pdf_status = False    

#Define thread 
LockRotary = threading.Lock() #maybe i dont need this?       

#Initialize interrupt handlers
def init():

	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(Enc_A, GPIO.IN) #PIN A (clk) is HIGH on default
	GPIO.setup(Enc_B, GPIO.IN) #PIN B (dt) is HIGH on default
	GPIO.setup(Enc_P, GPIO.IN) #Button of the Rotary Encoder
	GPIO.setup(But_B, GPIO.IN) #Back Button
	
	GPIO.add_event_detect(Enc_A, GPIO.FALLING, callback=rotary_interrupt) 	#No bouncetime on purpose!
	GPIO.add_event_detect(Enc_B, GPIO.FALLING, callback=rotary_interrupt)
	GPIO.add_event_detect(Enc_P, GPIO.FALLING, callback=button_interrupt)
	GPIO.add_event_detect(But_B, GPIO.FALLING, callback=button_interrupt)

#Function for opening the explorer
def openexplorer():
	p = Popen(['pcmanfm', '/home/pi/Recipes'])

#Define keypress function
def keypress(sequence):
	p = Popen(['xte', sequence])

#Define mapping function for keystrokes
def keymapping(key):
	global pdf_status
	if (key == "r" and pdf_status):
		for x in range(0, 14):
			keypress(d)
			x += 1
		keypress(c)
	elif (key == "r" and not pdf_status):
		keypress(r)
	elif (key == "l" and pdf_status):
		for x in range(0, 14):
			keypress(u)
			x += 1
	elif (key == "l" and not pdf_status):
		keypress(l)


#Define the interrupt actions --> this will be called on interrupts from A and B
def rotary_interrupt(A_or_B): 		#the interrupt passes the GPIO PIN number to the interrupt procedure
	global LockRotary
	
	#Read state of both switches
	Switch_A = GPIO.input(Enc_A)
	Switch_B = GPIO.input(Enc_B)

	if (not Switch_A and not Switch_B): 	#when both are closed, then end of sequence is reached
		LockRotary.acquire()
		checkxpdf()
		if A_or_B == Enc_B:
			print "right arrow pressed"
			keymapping("r")
		else:
			if A_or_B == Enc_A:
				print "left arrow pressed"
				keymapping("l")
		LockRotary.release()
	return

#Define the interrupt actions when button is pressed
def button_interrupt(button):
	global pdf_status

	#Wait a little bit, so that the RC components stop bouncing eachother
	sleep(0.05)
	
	#Check if pdf is opened in order to push the right buttons
	checkxpdf()
	
	#Check again the status of the buttons to be sure, which was pressed
	Status_P = GPIO.input(Enc_P)
	Status_B = GPIO.input(But_B)
	
	#Look which PIN caused callback and if callback PIN is still pressed
	if (button == Enc_P and not Status_P):
		keypress(e)
		print "Enter is pressed"
	elif (button == But_B and not Status_B and pdf_status):
		keypress('keydown Alt_L')
		keypress('key F4')
		keypress('keyup Alt_L')
		print "back for exit pressed"
	elif (button == But_B and not Status_B and not pdf_status):
		keypress(back)
		print "back pressed"
		
	return

#Define pdf-check function
def checkxpdf():
	global pdf_status
	
	p1 = Popen(["ps", "axg"], stdout=PIPE)
	p2 = Popen(["grep", "[x]pdf"], stdin=p1.stdout, stdout=PIPE)
	p1.stdout.close()
	(out, err) = p2.communicate()
	if out == "":
		pdf_status = False
	else:
		pdf_status = True
	print pdf_status

#start the functions
init()
openexplorer()
while True:
	sleep(0.01)
	
	
