#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import csv

#get win and lose from string
def getWinAndLose(str):
    number = '0123456789'
    flag = True  #flag to find win or lose
    win = ''
    lose = ''
    for char in str:
        if char in number:
            if flag:
                win = win + char
            else:
                lose = lose + char
        else:
            flag = False
    return win, lose

#translate origin data from csv to array data
def translateMatchOriginDataFactor(matchOriginData):
    matchDataFactor = []
    matchDataFactor.append(matchOriginData[0])  # AwayTeam Name
    matchDataFactor.append(matchOriginData[1])  # AtHomeTeam Name

    win, lose = getWinAndLose(matchOriginData[2])  # AwayTeam Match Data
    matchDataFactor.append(win)
    matchDataFactor.append(lose)

    win, lose = getWinAndLose(matchOriginData[3])  # AtHomeTeam Match Data
    matchDataFactor.append(win)
    matchDataFactor.append(lose)

    return matchDataFactor

def translateOriginMatchDataTrain(originMatchDataTrain):
    matchDataTrain = translateMatchOriginDataFactor(originMatchDataTrain)
    matchDataTrain.append(originMatchDataTrain[4].split(':')[0])  # AwayTeam Result
    matchDataTrain.append(originMatchDataTrain[4].split(':')[1])  # AtHomeTeam Result
    return matchDataTrain

def translateOriginMatchDataTest(originMatchDataTest):
    matchDataTest = translateMatchOriginDataFactor(originMatchDataTest)
    return matchDataTest

#get all data into array
def getMatchDataTrainList():
    csvFile = open("data/matchDataTrain.csv", "r")
    reader = csv.reader(csvFile)

    matchDataTrainList = []
    reader.next()  #Skip Line 1
    for originMatchDataTrain in reader:
        matchData = translateOriginMatchDataTrain(originMatchDataTrain)
        matchDataTrainList.append(matchData)

    csvFile.close()
    return matchDataTrainList

def getMatchDataTestList():
    csvFile = open("data/matchDataTest.csv", "r")
    reader = csv.reader(csvFile)

    matchDataTestList = []
    reader.next()  # Skip Line 1
    for originMatchDataTest in reader:
        matchData = translateOriginMatchDataTest(originMatchDataTest)
        matchDataTestList.append(matchData)

    csvFile.close()
    return matchDataTestList