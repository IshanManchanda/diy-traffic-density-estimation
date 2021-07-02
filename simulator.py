import os

from scheduler import Scheduler


def simulateSignal(inputPath):
    inputData = open(inputPath, 'r')
    outputFile = open(os.path.dirname(inputPath) + "/simulation_output.txt", "w")
    n_roads = 4
    n_lanes = [2, 2, 2, 2]
    k_c = 1
    k_w = 2
    k_a = 20
    schedulerObject = Scheduler(n_roads, n_lanes, k_c, k_a, k_w)
    # Initial random configuration
    whoGreen = 0
    accumulations = [0] * n_roads
    confirmation = False
    lineArray = [line.split() for line in inputData]
    i = 0
    while i < len(lineArray):
        if confirmation:
            outputFile.write(f"Road {whoGreen} is shown the green signal {i}\n")
            accumulations[whoGreen] -= n_lanes[whoGreen]

            increase = [int(j) for j in lineArray[i]]
            assert len(increase) == len(accumulations)
            for k in range(len(accumulations)):
                accumulations[k] += increase[k]
            if accumulations[whoGreen] < 0:
                accumulations[whoGreen] = 0
            transition, confirmation, road_index = schedulerObject.update(accumulations)
            if transition:
                whoGreen = road_index
            i += 1

        elif i + 1 < len(lineArray):
            outputFile.write(f"Road {whoGreen} is shown the green signal {i}\n")
            outputFile.write(f"Road {whoGreen} is shown the green signal {i}\n")
            accumulations[whoGreen] -= n_lanes[whoGreen] * 2

            increase1 = [int(j) for j in lineArray[i]]
            increase2 = [int(j) for j in lineArray[i + 1]]
            for k in range(len(accumulations)):
                accumulations[k] += increase1[k] + increase2[k]
            if accumulations[whoGreen] < 0:
                accumulations[whoGreen] = 0
            transition, confirmation, road_index = schedulerObject.update(accumulations)
            if transition:
                whoGreen = road_index
            i += 2
        else:
            break
    return True
