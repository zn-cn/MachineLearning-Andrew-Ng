#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import csv
import random

csvFile = open("data/teamData.csv", "r")
reader = csv.reader(csvFile)

#translate origin data from csv to array data
def translateTeamOriginData(teamOriginData):
    teamData = []
    teamData.append(teamOriginData[0])  # Team Name
    teamData.append(teamOriginData[1])  # Member Name

    teamData.append(teamOriginData[3])  # starting times
    teamData.append(teamOriginData[2])  # on times
    teamData.append(teamOriginData[4])  # time

    teamData.append(teamOriginData[6])  # field goal times
    teamData.append(teamOriginData[7])  # field times

    teamData.append(teamOriginData[9])  # three shot goal times
    teamData.append(teamOriginData[10])  # three shot times

    teamData.append(teamOriginData[12])  # free throw goal times
    teamData.append(teamOriginData[13])  # free throw times

    teamData.append(teamOriginData[14])  # rebound
    teamData.append(teamOriginData[15])  # offensive rebound
    teamData.append(teamOriginData[16])  # defensive rebound

    teamData.append(teamOriginData[17])  # assist
    teamData.append(teamOriginData[18])  # ST
    teamData.append(teamOriginData[19])  # block shot
    teamData.append(teamOriginData[20])  # turn over
    teamData.append(teamOriginData[21])  # PF

    teamData.append(teamOriginData[22])  # scoring

    return teamData

#get all data into array
def getAllTeamData():
    teamDataArray = []
    reader.next()  #Skip Line 1
    for teamOriginData in reader:
        teamData = translateTeamOriginData(teamOriginData)
        teamDataArray.append(teamData)
    return teamDataArray