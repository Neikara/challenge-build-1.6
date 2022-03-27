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

	"""def inDanger(projectile):
		xPro = projectile.position[0]
		yPro = projectile.position[1]
		xSpeed = projectile.speed[0]
		ySpeed = projectile.speed[1]
		angle = (-math.copysign(1,xPro-xMe)*90+90)+arctan(ySpeed/xSpeed)*180/3.14
		if (xMe - xPro)*(xMe - xPro)+(yMe - yPro)*(yMe - yPro) <36000 and angle > :
			pass
	  
	def esquive():
		for projectile in gamestate.projectiles:
			if inDanger(projectile):
				projectile.position
			else:
				pass"""
	
	
	if my_data.get('first') is None:
		if xMe < -20.0:
			my_data['first'] = 1
		else:
			my_data['first'] = 0
	meCenter = zone(xMe, yMe) == "Center"
	himCenter = zone(xHim, yHim) == "Center"
	if healthHim < 0:
		if scoreHim < scoreMe and not zone(xMe,yMe) == "CornerLeftAlmostUp" and not zone(xMe,yMe) == "CornerDownAlmostRight":
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
	return MoveCommand((0.0, 1.0, 0.0))


if __name__ == '__main__':
	simulation_list = []
	used_port = 2049

	simulation = GameSimulation('java', game_time=60.0, ai_time=150.0, commands_per_second=4.0, port=used_port)

	first_agent_data = {}
	second_agent_data = {}

	simulation.set_first_agent('agent_0', my_ai, first_agent_data)
	simulation.set_second_agent('agent_1', my_ai, second_agent_data)

	simulation.start_round()

	results, data = simulation.end_round()

	for agent_result in results:
		print(f'Agent result: {agent_result}')

	for agent_data in data:
		print(f'Agent data: {agent_data}')
		
