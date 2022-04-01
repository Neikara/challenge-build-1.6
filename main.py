from lib2to3.pytree import HUGE

from numpy import arctan
from game_simulation import GameSimulation, SnapshotData
from agent import InvalidCommand, MoveCommand, ShootCommand, Command
import typing
import random
import math
import time

def my_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	scoreMe = gamestate.controlled_player.score
	scoreHim = gamestate.other_players[0].score
	healthMe = gamestate.controlled_player.health
	healthHim = gamestate.other_players[0].health
	xMe = gamestate.controlled_player.position[0]
	yMe = gamestate.controlled_player.position[1]
	xHim = gamestate.other_players[0].position[0]
	yHim = gamestate.other_players[0].position[1]
 
	def moveTo(x,y):
		if esquive() != -1:
			projectile = gamestate.projectiles[esquive()]
			lol = bool(random.getrandbits(1))
			if lol:
				return MoveCommand((projectile.speed[1]/300, -projectile.speed[0]/300,0.0))
			else:
				return MoveCommand((-projectile.speed[1]/300, projectile.speed[0]/300,0.0))
		if y==yMe and x==xMe:
			return ShootCommand(0.0)
		if x==xMe:
			return MoveCommand((0.0,math.copysign(1.0,y-yMe),0.0))
		if y==yMe:
			return MoveCommand((math.copysign(1.0,x-xMe),0.0,0.0))
		return MoveCommand(((x-xMe)/math.sqrt((xMe-x)*(xMe-x)+(yMe-y)*(yMe-y)), (y-yMe)/math.sqrt((xMe-x)*(xMe-x)+(yMe-y)*(yMe-y)),0.0))
	
	def zone(x,y):
			if y > 216:
				if x < -216:
					return "CornerUpLeft"
				elif x < -34:
					return "CornerUpAlmostLeft"
				elif x < 216:
					return "CenterUp"
				else:
					return "CornerUpRight"
			elif y > 0 and x < -216:
				return "CornerLeftAlmostUp"
			elif y < 0 and x > 216:
				return "CornerRightAlmostDown"
			elif y < -216:
				if x > 216:
					return "CornerDownRight"
				elif x > 34:
					return "CornerDownAlmostRight"
				elif x >-216:
					return "CenterDown"
				else:
					return "CornerDownLeft"
			elif x < 100 and x >-100 and y > -100 and y < 100:
				return "Center"
			return "Middle"

	def inDanger(projectile):
		if healthHim > 0 and healthMe >0:
			xPro = projectile.position[0]
			yPro = projectile.position[1]
			xSpeed = projectile.speed[0]
			ySpeed = projectile.speed[1]
			if xSpeed !=0:
				angleTir = (-math.copysign(1,xSpeed)*90+90)+arctan(ySpeed/xSpeed)*180/3.14
			if (xPro-xMe)!=0:
				angleMe = (-math.copysign(1,xPro-xMe)*90+90)+arctan((yMe-yPro)/(xPro-xMe+0.001))*180/3.14
			if xSpeed==0:
				angleTir = math.copysign(90,ySpeed)
				angleMe = (-math.copysign(1,xPro-xMe)*90+90)+arctan((yMe-yPro)/(xPro-xMe+0.001))*180/3.14
			else:
				angleTir = math.copysign(90,ySpeed)+90
				angleMe = (-math.copysign(1,xPro-xMe)*90+90)+arctan((yMe-yPro)/(xPro-xMe+0.001))*180/3.14
			if angleTir<0:
				angleTir+=360
			if angleMe<0:
				angleMe+=360
			rayon_carré = (xMe - xPro)*(xMe - xPro)+(yMe - yPro)*(yMe - yPro)
			if math.sqrt(rayon_carré) <72000 and abs(angleTir-angleMe) > 160 and abs(angleTir-angleMe) < 200:
				return True
			else:
				return False
		else:
			return False
		
	def esquive():
		for i in range(len(gamestate.projectiles)):
			if inDanger(gamestate.projectiles[i]):
				return i
		return -1
	
	if my_data.get('first') is None:
		if xMe < -20.0:
			my_data['first'] = 1
		else:
			my_data['first'] = 0
	meCenter = zone(xMe, yMe) == "Center"
	himCenter = zone(xHim, yHim) == "Center"
	 
	if healthHim < 0:
		if scoreHim + 10 < scoreMe and not zone(xMe,yMe) == "CornerLeftAlmostUp" and not zone(xMe,yMe) == "CornerDownAlmostRight":
			if zone(xMe,yMe) == "CornerUpRight":
				if my_data.get('first') == 1:
					return ShootCommand(-90)
				else:
					return ShootCommand(180)
			else:
				return moveTo(250,250)
		elif zone(xMe,yMe) == "CornerUpLeft":
			return moveTo(-250,0)
		elif zone(xMe,yMe) == "CornerDownRight":
			return moveTo(250,0)
		return moveTo(0,0)
	elif meCenter and not himCenter:
		return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
	elif not meCenter and not himCenter:
		if (zone(xMe,yMe) == "CornerUpLeft" and (zone(xHim,yHim) == "CornerUpRight" or zone(xHim,yHim) == "CornerUp")):
			return moveTo(-250,0)
		elif (zone(xMe,yMe) == "CornerUpLeft" and (zone(xHim,yHim) == "CornerUpAlmostLeft" or zone(xHim,yHim) == "CornerDownLeft")):
			return moveTo(0,250)
		elif (zone(xMe,yMe) == "CornerDownRight" and (zone(xHim,yHim) == "CornerUpRight" or zone(xHim,yHim) == "CornerRightAlmostDown")):
			return moveTo(0,-250)
		elif (zone(xMe,yMe) == "CornerDownRight" and (zone(xHim,yHim) == "CornerDownLeft" or zone(xHim,yHim) == "CornerUpAlmostLeft")):
			return moveTo(250,0)
		else:
			if zone(xMe,yMe) == "CornerUpLeft" or zone(xMe,yMe) == "CornerLeftAlmostUp":
				return moveTo(-250,0)
			if zone(xMe,yMe) == "CornerDownRight" or zone(xMe,yMe) == "CornerRightAlmostDown":
				return moveTo(250,0)
			return moveTo(0,0)
	elif not meCenter and himCenter:
		if zone(xMe,yMe) == "CornerUpLeft" or zone(xMe,yMe) == "CornerLeftAlmostUp":
			return moveTo(-250,0)
		if zone(xMe,yMe) == "CornerDownRight" or zone(xMe,yMe) == "CornerRightAlmostDown":
			return moveTo(250,0)
		return moveTo(0,0)
	elif meCenter and himCenter:
		return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
	"""
	def increase_right(data):
		if data.get('right') is None:
			data['right'] = 1
		else:
			data['right'] += 1
	"""
	return ShootCommand(45.0)

def idle_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	scoreMe = gamestate.other_players[0].score
	scoreHim = gamestate.controlled_player.score
	healthMe = gamestate.other_players[0].health
	healthHim = gamestate.controlled_player.health
	xMe = gamestate.controlled_player.position[0]
	yMe = gamestate.controlled_player.position[1]
	xHim = gamestate.other_players[0].position[0]
	yHim = gamestate.other_players[0].position[1]

	def moveTo(position: str):
		try:
			position = positions(position)
			positionX, positionY = position
			if yMe>positionY-16 and yMe<positionY+16 and xMe>positionX-16 and xMe<positionX+16:
				return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
			elif positionX==xMe:
				return MoveCommand((0.0,math.copysign(1.0,positionY-yMe),0.0))
			elif positionY==yMe:
				return MoveCommand((math.copysign(1.0,positionX-xMe),0.0,0.0))
			return MoveCommand(((positionX-xMe)/math.sqrt((xMe-positionX)*(xMe-positionX)+(yMe-positionY)*(yMe-positionY)), 
						(positionY-yMe)/math.sqrt((xMe-positionX)*(xMe-positionX)+(yMe-positionY)*(yMe-positionY)),0.0))
		except:
			return MoveCommand((0.0,0.0,0.0))
			
  
	def zone(x,y):
		"""This function returns the zone where the player is

		Args:
			x (float): x coordinate of the player
			y (float): y coordinate of the player

		Returns:
			str: the name of zone where the player is.
		RED ZONE(50x50): Spawn zone
		GREEN ZONE(182x50): Safe Zone Behind Wall X
		YELLOW ZONE(236x50): Exposed/Transition Zone X
		BLUE ZONE(82x135): Combat Zone
		ORANGE ZONE(50x182): Exposed/Transition Zone Y
		PURPLE ZONE(182x50): Safe Zone Behind Wall Y
		WHITE ZONE(200x200): Center Zone
		BLACK ZONE: no zone
		"""
		if (y>225 and y<275) or (y<-225 and y>-275):
			if (x>-275 and x<-225) or (x>225 and x<275):
				return "Red"
			elif (x>-225 and x<-43) or (x>43 and x<225):
				return "Green"
			elif (x>-43 and x<193) or (x>-193 and x<43):
				return "Yellow"
		elif (y>140 and y<275) or (y<-140 and y>-275):
			if (x>193 and x<275) or (x>-275 and x<-193):
				return "Blue"
		elif (y<43 and y>-139) or (y<139 and y>-43):
			if (x>-275 and x<225) or (x>225 and x<275):
				return "Orange"
		elif (y>43 and y<225) or (y>-225 and y<-43):
			if (x>-275 and x<225) or (x>225 and x<275):
				return "Purple"
		elif x < 100 and x >-100 and y > -100 and y < 100:
			return "White"
		return "Black"

	def positions(pos):
		"""This function returns the coordinates of the strategic points in the game."""
		pos_dict = {"A1_1":(250,250), "A1_2": (-250, -250),
              "G1_1":(-165, 250), "G2_1": (-104, 250), "G1_2": (104, -250), "G2_2": (165, -250),
              "Y1_1": (36, 250), "Y2_1": (115, 250), "Y1_2": (-36, -250), "Y2_2": (-115, -250),
              "B1_1": (221, 230), "B2_1": (248, 185), "B1_2": (-221, -230), "B2_2": (-248, -185),
              "O1_1": (-250, -18), "O2_1": (-250, -79), "O1_2": (250, 79), "O2_2": (250, 18),
              "P1_1": (250, -165), "P2_1": (250, -104), "P1_2": (-250, 104), "P2_2": (-250, 165),
              "W1_1": (75, 75), "W2_1": (-75, -75)}
		return pos_dict[pos]
	
	if healthMe > 0:
		if healthHim < 0:
			return moveTo("W1_2")
		else:
			chance = bool(random.getrandbits(1))
			if chance:
				return moveTo('O1_2')
			else:
				return moveTo('O2_2')
	else:
		return moveTo("W1_1")

		
	


if __name__ == '__main__':
	simulation_list = []
	used_port = 2049

	simulation = GameSimulation('java', game_time=60.0, ai_time=150.0, commands_per_second=4.0, port=used_port)

	first_agent_data = {}
	second_agent_data = {}

	simulation.set_first_agent('agent_0', my_ai, first_agent_data)
	simulation.set_second_agent('agent_1', idle_ai, second_agent_data)

	simulation.start_round()

	results, data = simulation.end_round()

	for agent_result in results:
		print(f'Agent result: {agent_result}')

	for agent_data in data:
		print(f'Agent data: {agent_data}')
		
