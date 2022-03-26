from lib2to3.pytree import HUGE

from numpy import arctan
from game_simulation import GameSimulation, SnapshotData
from agent import InvalidCommand, MoveCommand, ShootCommand, Command
import typing
import random
import math
import time

def my_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	def moveTo(x,y,xMe, yMe):
		if x==xMe:
			return MoveCommand((0.0,math.copysign(1,yMe-y),0.0))
		if y==yMe:
			return MoveCommand((math.copysign(1,xMe-x),0.0,0.0))
		return MoveCommand(((x-xMe)/math.sqrt((xMe-x)*(xMe-x)+(yMe-y)*(yMe-y)), (y-yMe)/math.sqrt((xMe-x)*(xMe-x)+(yMe-y)*(yMe-y)),0.0))
	def inZone(down,up,left,right,x,y):
		if x < right and x > left and y < up and y > down:
			return True
		return False
	scoreMe = gamestate.controlled_player.score
	scoreHim = gamestate.other_players[0].score
	healthMe = gamestate.controlled_player.health
	healthHim = gamestate.other_players[0].health
	xMe = gamestate.controlled_player.position[0]
	yMe = gamestate.controlled_player.position[1]
	xHim = gamestate.other_players[0].position[0]
	yHim = gamestate.other_players[0].position[1]
	gamestate.projectiles
	meCenter = inZone(-100,100,-100,100,xMe, yMe)
	himCenter = inZone(-100,100,-100,100,xHim, yHim)
	if healthHim < 0:
		if scoreHim < scoreMe:
			if inZone(216,275,216,275,xMe,yMe):
				return ShootCommand(-90)
			else :
				return moveTo(250,250,xMe,yMe)
		else:
			return moveTo(0,0,xMe,yMe)
	elif meCenter and not himCenter:
		return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
	elif not meCenter and not himCenter:
		if (inZone(-275,0,216,275,xMe,yMe) and inZone(0,275,-275,-216,xHim,yHim)) or (inZone(-275,0,216,275,xHim,yHim) and inZone(0,275,-275,-216,xMe,yMe)):
			return moveTo(0,0,xMe,yMe)
		if (inZone(216,275,216,275,xMe,yMe) and inZone(-275,0,216,275,xHim,yHim)) or (inZone(216,275,216,275,xMe,yMe) and inZone(-275,0,-275,-216,xHim,yHim)):
			return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
		else: 
			moveTo(-250,0,xMe, yMe)
	elif not meCenter and himCenter:
		if inZone(-275,0,216,275,xMe,yMe):
			return moveTo(250,0,xMe,yMe)
		if inZone(0,275,-275,-216,xMe,yMe):
			return moveTo(-250,0,xMe,yMe)
		return moveTo(0,0,xMe,yMe)
	elif meCenter and himCenter:
		return ShootCommand((-math.copysign(1,xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)
	"""
	def increase_right(data):
		if data.get('right') is None:
			data['right'] = 1
		else:
			data['right'] += 1

	x = gamestate.controlled_player.position[0]
	y = gamestate.controlled_player.position[1]
	increase_right(my_data)
	if x < 0:
		return MoveCommand((1.0, 0.0, 0.0))
	elif y > 0:
		return MoveCommand((0.0, -1.0, 0.0))
	else:
		return ShootCommand(45.0)
#		return MoveCommand((0.0, 0.0, 0.0))
  	"""
	return ShootCommand(45.0)

def idle_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	return MoveCommand((0.0, 1.0, 0.0))


if __name__ == '__main__':
	simulation_list = []
	used_port = 2049

	simulation = GameSimulation('java', game_time=20.0, ai_time=150.0, commands_per_second=4.0, port=used_port)

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
        
