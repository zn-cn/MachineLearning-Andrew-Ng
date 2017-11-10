#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import matchDataInit
import teamDataInit

import tensorflow as tf
import random
import csv

####整理数据###################

def getMatchDataTrainList():
    matchDataTrainList = []
    originDataList = matchDataInit.getMatchDataTrainList()
    for originData in originDataList:
        matchData = []
        for data in originData:
            matchData.append(int(data))
        matchDataTrainList.append(matchData)
    return matchDataTrainList

def getMatchDataTestList():
    matchDataTestList = []
    originDataList = matchDataInit.getMatchDataTestList()
    for originData in originDataList:
        matchData = []
        for data in originData:
            matchData.append(int(data))
        matchDataTestList.append(matchData)
    return matchDataTestList

def getTeamDataList():
    teamDataList = []
    teamSumData = [0.0 for i in range(15)]
    originDataList = teamDataInit.getAllTeamData()
    for i in range(208):
        teamPlayerList = []
        for originData in originDataList:
            if (int(originData[0]) == i):
                playerData = []
                for key in range(2, 20):
                    playerData.append(float(originData[key]))
                teamPlayerList.append(playerData)
        teamPlayerList.sort(key = lambda x:x[2], reverse = True)

        teamData = [0.0 for i in range(15)]
        for playerKey in range(4):
            for dataKey in range(3, 18):
                teamData[dataKey-3] += teamPlayerList[playerKey][dataKey]
                teamSumData[dataKey-3] += teamPlayerList[playerKey][dataKey]
        teamDataList.append(teamData)
    for teamData in teamDataList:
        for key in range(15):
            teamData[key] = teamData[key] * 208 / teamSumData[key]
    return teamDataList

# 提取列表原始数据
matchDataTrainList = getMatchDataTrainList()[0 : 6000]
matchDataTestList = getMatchDataTrainList()[6000 : 7000]

teamDataList = getTeamDataList()

def getWinRate(win, lose):
    if ((win + lose) == 0):
        return 0.5
    else:
        return (win + 0.0) / (win + lose)

def getMatchFactor(matchData):
    matchFactor = []
    for key in range(15):
        matchFactor.append(teamDataList[matchData[0]][key])
        matchFactor.append(teamDataList[matchData[1]][key])
    matchFactor.append(getWinRate(matchData[2], matchData[3]) / 0.5)
    matchFactor.append(getWinRate(matchData[4], matchData[5]) / 0.5)
    return matchFactor

def getMatchFactorList(matchDataList):
    matchFactorList = []
    for matchData in matchDataList:
        matchFactorList.append(getMatchFactor(matchData))
    return matchFactorList

def getMatchResultList(matchDataList):
    matchResultList = []
    for matchData in matchDataList:
        if (matchData[7] > matchData[6]):
            matchResultList.append([1.0, 0.0])
        else:
            matchResultList.append([0, 1.0])
    return matchResultList

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def add_layer(inputs, in_size, out_size, activation_function=None):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# 获取一定数量的随机数据
def getRandomData(number):
    randomMatchDataList = random.sample(matchDataTrainList, number)
    randomMatchFactorList = getMatchFactorList(randomMatchDataList)
    randomMatchResultList = getMatchResultList(randomMatchDataList)
    return randomMatchFactorList, randomMatchResultList

x = tf.placeholder("float", shape=[None, 32])

W_matmul1 = weight_variable([32, 64])
b_matmul1 = bias_variable([64])

h_matmul1 = tf.nn.sigmoid(tf.matmul(x, W_matmul1) + b_matmul1)

W_matmul2 = weight_variable([64, 128])
b_matmul2 = bias_variable([128])

h_matmul2 = tf.nn.sigmoid(tf.matmul(h_matmul1, W_matmul2) + b_matmul2)

W_matmul3 = weight_variable([128, 64])
b_matmul3 = bias_variable([64])

h_matmul3 = tf.nn.sigmoid(tf.matmul(h_matmul2, W_matmul3) + b_matmul3)

keep_prob = tf.placeholder("float")
h_matmul3_drop = tf.nn.dropout(h_matmul3, keep_prob)

W_fc1 = weight_variable([64, 2])
b_fc1 = bias_variable([2])

y = tf.nn.softmax(tf.matmul(h_matmul3_drop, W_fc1) + b_fc1)

y_ = tf.placeholder("float", shape=[None, 2])
cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))

train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

for i in range(20000):
    batch_xs, batch_ys = getRandomData(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 0.5})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
data_xs = getMatchFactorList(matchDataTestList)
data_ys = getMatchResultList(matchDataTestList)
print (sess.run(accuracy, feed_dict={x: data_xs, y_: data_ys, keep_prob: 1.0}))


matchDataTestList = getMatchDataTestList()
data_xs = getMatchFactorList(matchDataTestList)
out = sess.run(y, feed_dict={x: data_xs, keep_prob: 1.0})
print out

predict = []
for data in out:
    predict.append([data[0]]);

csvFile = open("predict.csv", "w")
writer = csv.writer(csvFile)
writer.writerows(predict)
csvFile.close()
# sess = tf.InteractiveSession()
# a = tf.Print(a, [a], message="This is a: ")
# b = tf.add(a, a).eval()