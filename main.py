from scheduler import Scheduler
import numpy as np
def main():
	inputData = open('schedulerData.txt', 'rt')
	
	n_roads = 4
	n_lanes = 2
	k_c = 1
	k_w = 2
	k_a = 1.5
	schedulerObject = Scheduler(n_roads, n_lanes, k_c, k_a, k_w)
	# Initial random configuration
	whoGreen = 0
	accumulations = [0] * n_roads
	confirmation = False
	lineArray = [line.split() for line in inputData]
	i = 0
	while i < len(lineArray):
		if confirmation:
			print(f"Road {whoGreen} is shown the green signal")
			accumulations[whoGreen] -= n_lanes
			if accumulations[whoGreen] < 0:
				accumulations[whoGreen] = 0
			increase = [int(j) for j in lineArray[i]]
			assert len(increase) == len(accumulations)
			for k in range(len(accumulations)):
				accumulations[k] += increase[k]
			transition, confirmation, road_index = schedulerObject.update(accumulations)
			if transition:
				whoGreen = road_index
			i += 1

		elif i+1 < len(lineArray):
			print(f"Road {whoGreen} is shown the green signal")
			print(f"Road {whoGreen} is shown the green signal")
			accumulations[whoGreen] -= n_lanes * 2
			if accumulations[whoGreen] < 0:
				accumulations[whoGreen] = 0
			increase1 = [int(j) for j in lineArray[i]]
			increase2 = [int(j) for j in lineArray[i+1]]
			for k in range(len(accumulations)):
				accumulations[k] += increase1[k] + increase2[k]
			transition, confirmation, road_index = schedulerObject.update(accumulations)
			if transition:
				whoGreen = road_index
			i += 2



if __name__ == '__main__':
	main()
