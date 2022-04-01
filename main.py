
from logging import exception
from numpy import arctan
from game_simulation import GameSimulation, SnapshotData
from agent import InvalidCommand, MoveCommand, ShootCommand, Command
import typing
import random
import math
import competitionAI


def my_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	return competitionAI.my_ai(gamestate, my_data)


def idle_ai(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
	scoreMe = gamestate.other_players[0].score
	scoreHim = gamestate.controlled_player.score
	healthMe = gamestate.other_players[0].health
	healthHim = gamestate.controlled_player.health
	xMe = gamestate.controlled_player.position[0]
	yMe = gamestate.controlled_player.position[1]
	xHim = gamestate.other_players[0].position[0]
	yHim = gamestate.other_players[0].position[1]
	my_data["status"] = "attacking"
	status = my_data["status"]

	def shoot():
		return ShootCommand((-math.copysign(1, xHim-xMe)*90+90)+arctan((yHim-yMe)/(xHim-xMe))*180/3.14)

	def moveTo(position: str):
		try:
			position = positions(position)
			positionX, positionY = position
			if xMe > positionX-16 and xMe < positionX+16:  # correct positionX but not positionY
				return MoveCommand((0.0, math.copysign(1.0, positionY-yMe), 0.0))
			elif yMe > positionY-16 and yMe < positionY+16:  # correct positionY but not positionX
				return MoveCommand((math.copysign(1.0, positionX-xMe), 0.0, 0.0))
			else:  # not in position -> move to position in straigth line
				vX = (positionX-xMe)/math.sqrt((xMe-positionX) *
											   (xMe-positionX)+(yMe-positionY)*(yMe-positionY))
				vY = (positionY-yMe)/math.sqrt((xMe-positionX) *
											   (xMe-positionX)+(yMe-positionY)*(yMe-positionY))
				return MoveCommand((vX, vY, 0.0))
		except:
			return MoveCommand((0.0, 0.0, 0.0))

	def zone(x, y):
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
		if (y > 225 and y < 275) or (y < -225 and y > -275):
			if (x > -275 and x < -225) or (x > 225 and x < 275):
				return "Red"
			elif (x > -225 and x < -43) or (x > 43 and x < 225):
				return "Green"
			elif (x > -43 and x < 193) or (x > -193 and x < 43):
				return "Yellow"
		elif (y > 140 and y < 275) or (y < -140 and y > -275):
			if (x > 193 and x < 275) or (x > -275 and x < -193):
				return "Blue"
		elif (y < 43 and y > -139) or (y < 139 and y > -43):
			if (x > -275 and x < 225) or (x > 225 and x < 275):
				return "Orange"
		elif (y > 43 and y < 225) or (y > -225 and y < -43):
			if (x > -275 and x < 225) or (x > 225 and x < 275):
				return "Purple"
		elif x < 100 and x > -100 and y > -100 and y < 100:
			return "White"
		elif (x > -225 and x < -43) or (x > 43 and x < 225):
			if (y > 193 and y < 225) and (y > -193 and y < -225):
				return "WallX"
		elif (x > -193 and x < -225) or (x > 193 and x < 225):
			if (y > 43 and y < 225) and (y > -43 and y < -225):
				return "WallY"
		return "Black"

	def positions(pos):
		"""This function returns the coordinates of the strategic points in the game."""
		pos_dict = {"R1_1": (-250, 250), "R1_2": (250, -250),
					"G1_1": (-165, 250), "G2_1": (-104, 250), "G1_2": (104, -250), "G2_2": (165, -250),
					"Y1_1": (36, 250), "Y2_1": (115, 250), "Y1_2": (-36, -250), "Y2_2": (-115, -250),
					"B1_1": (221, 230), "B2_1": (248, 185), "B1_2": (-221, -230), "B2_2": (-248, -185),
					"O1_1": (-250, -18), "O2_1": (-250, -79), "O1_2": (250, 79), "O2_2": (250, 18),
					"P1_1": (250, -165), "P2_1": (250, -104), "P1_2": (-250, 104), "P2_2": (-250, 165),
					"W1_1": (-75, 75), "W1_2": (75, -75)}
		if type(pos) == str:
			return pos_dict[pos]
		elif type(pos) == tuple:
			res = [k for k, v in pos_dict.items() if (
				(v[0] + 32 > pos[0] and v[0] - 32 < pos[0]) and (v[1] + 32 > pos[1] and v[1] - 32 < pos[1]))]
			return res[0]
		else:
			raise Exception("pos must be a tuple or a string")

	def amIFirst(x, y):
		"""Returns True if the player is the first player which means that he started at top left (-250, 250)

		Args:
										x (float): x coordinates of the player
										y (float): x coordinates of the player
		"""
		if "player number" in my_data:
			return True
		else:
			position = positions((x, y))
			if position == "R1_1":
				my_data["player number"] = 0
			else:
				my_data["player number"] = 1
		return 0

	def randomChoice2():
		"""Returns a random choice between two options"""
		return random.choice([True, False])

	def randomChoice3():
		"""Returns a random choice between Three options"""
		return random.choice([True, False, True])

	def setStatus(newStatus: str):
		if newStatus in ["attacking", "defending", "neutral", "retreating"]:
			my_data["status"] = newStatus
		else:
			my_data["status"] = "attacking"
		return 0

	if amIFirst(xMe, yMe) == True:  # whether the player is top left or bottom right
		if healthHim < 0:  # if enemy is dead
			setStatus("neutral")
			return moveTo("W1_1")  # go to center
		else:
			if zone(xMe, yMe) == "Red":  # if player is in red zone
				"""choice = randomChoice2()"""
				choice = True
				if choice:  # get a random choice between two possible options
					return moveTo("G1_1")
				else:
					return moveTo("P1_1")

			elif zone(xMe, yMe) == "Green":  # if player is in green zone
				if status == "attacking" and healthHim > 0:  # if player is attacking
					if healthMe >= 0.75*healthMe:  # if player is strong enough
						return moveTo("Y1_1")
					else:  # if player is not strong enough
						setStatus("defending")
						return moveTo("G2_1")  # TODO
				elif status == "defending":
					return moveTo("G1_1")  # get cover
				elif status == "retreating":  # if player is retreating
					return moveTo("R1_1")  # go to red zone
				else:
					return moveTo("W1_1")  # neutral: focus objective

			elif zone(xMe, yMe) == "Yellow":  # if player is in yellow zone
				if status == "attacking" and healthHim > 0:  # if player is attacking
					if healthMe >= 0.50*healthMe:  # if player is strong enough
						for i in [1, 1, 0]:
							if i==1:
								return shoot()
							else:
								if positions((xMe, yMe)) == "Y1_1":
									return moveTo("Y2_1")
								else:
									return moveTo("Y1_1")
					else:  # if player is not strong enough
						setStatus("defending")  # get cover
						return shoot()  # TODO
				elif status == "defending" and healthHim > 0:
					if healthMe >= 0.20*healthMe:
						if randomChoice2():  # Randomly choose between two options
							return moveTo("B1_1")
						else:
							return moveTo("B2_1")
					else:
						setStatus("retreating")  # Retreat
						return shoot() #TODO
				elif status == "retreating" and healthHim > 0:  # if player is retreating
					return moveTo("G2_1")
				else:  # neutral: focus objective
					return moveTo("W1_1")

			elif zone(xMe, yMe) == "Blue":
				if status == "attacking":
					return moveTo("Y1_1")
				elif status == "defending":
					return moveTo("G1_1")
				else:
					return moveTo("G2_1")
			elif zone(xMe, yMe) == "Orange":
				if status == "attacking":
					return moveTo("Y1_1")
				elif status == "defending":
					return moveTo("G1_1")
				else:
					return moveTo("G2_1")
			elif zone(xMe, yMe) == "Purple":
				if status == "attacking":
					return moveTo("Y1_1")
				elif status == "defending":
					return moveTo("G1_1")
				else:
					return moveTo("G2_1")
			elif zone(xMe, yMe) == "White":
				if status == "attacking":
					return moveTo("Y1_1")
				elif status == "defending":
					return moveTo("G1_1")
				else:
					return moveTo("G2_1")
			elif zone(xMe, yMe) == "Black":
				if status == "attacking":
					return moveTo("Y1_1")
				elif status == "defending":
					return moveTo("G1_1")
				else:
					return moveTo("G2_1")
	else:  # if player is bottom right
		if healthHim <= 0:  # if enemy is dead
			setStatus("neutral")
			return moveTo("W1_1")  # go to center
		else:
			if zone(xMe, yMe) == "Red":  # if player is in red zone
				choice = randomChoice2()
				if choice:  # get a random choice between two possible options
					return moveTo("G2_2")
				else:
					return moveTo("P2_2")
			elif zone(xMe, yMe) == "Green":  # if player is in green zone
				if status == "attacking":  # if player is attacking
					if healthMe >= 0.75*healthHim:  # if player is strong enough
						return moveTo("Y1_2")  # go to yellow zone
					else:
						# if player is not strong enough
						setStatus("defending")
						return moveTo("G1_2")  # get cover
				elif status == "defending":  # if player is defending
					return moveTo("R1_2")  # go to red zone
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "Yellow":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "Blue":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "Orange":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "Purple":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "White":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
			elif zone(xMe, yMe) == "Black":
				if status == "attacking":
					return moveTo("Y1_2")
				elif status == "defending":
					return moveTo("G1_2")
				else:
					return moveTo("G2_2")
		


if __name__ == '__main__':
	simulation_list = []
	used_port = 2049

	simulation = GameSimulation(
		'java', game_time=60.0, ai_time=150.0, commands_per_second=4.0, port=used_port)

	first_agent_data = {}
	second_agent_data = {}

	simulation.set_first_agent('agent_0', idle_ai, first_agent_data)
	simulation.set_second_agent('agent_1', my_ai, second_agent_data)

	simulation.start_round()

	results, data = simulation.end_round()

	for agent_result in results:
		print(f'Agent result: {agent_result}')

	for agent_data in data:
		print(f'Agent data: {agent_data}')
