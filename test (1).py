import RPi.GPIO as GPIO
import keyboard

class Motor:
	def __init__(self,a:int,b:int):
		self.a_pin = a
		self.b_pin = b
		GPIO.setmode(GPIO.BCM)
		
		GPIO.setup(self.a_pin,GPIO.OUT)
		self.pwm_a = GPIO.PWM(self.a_pin,1000)
		GPIO.setup(self.b_pin,GPIO.OUT)
		self.pwm_b = GPIO.PWM(self.b_pin,1000)
	
	def move(self,power):		
		self.pwm_a.start(power if power > 0 else 0)
		self.pwm_b.start(-power if power < 0 else 0)

	def __del__(self):
		GPIO.cleanup([self.a_pin,self.b_pin])
		

def main():
	print("running")
	motor_a = Motor(18,12)
	motor_b = Motor(19,13)
	
	while True:
		if keyboard.is_pressed('w'):
			print('w')
			motor_a.move(80)
			motor_b.move(80)
		elif keyboard.is_pressed('a'):
			print('a')
			motor_a.move(0)
			motor_b.move(80)
		elif keyboard.is_pressed('d'):
			print('d')
			motor_a.move(80)
			motor_b.move(0)
		elif keyboard.is_pressed('s'):
			print('s')
			motor_a.move(-80)
			motor_b.move(-80)
		else:
			print('end')
			motor_a.move(0)
			motor_b.move(0)
	
	del motor_a, motor_b
	
if __name__ == '__main__':
	main()
