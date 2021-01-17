import PySimpleGUI as sg
import pandas as pd
import os

def clearscreen():
	os.system("cls")

def makeTable(probeIDList, failureList):
	data = {	"ProbeID"		:	probeIDList,
				"FailureMode"	:	failureList,
		}

	clearscreen()

	df = pd.DataFrame(data)
	
	print(df.to_string(index=False))

def deleteOneEntry(probeIDList, failureList):
	clearscreen()
	probeIDList.pop(-1)
	failureList.pop(-1)

def deleteAllEntries(probeIDList, failureList):
	clearscreen()
	probeIDList.clear()
	failureList.clear()

def storeTable(probeIDList, failureList):
	data = {	"ProbeID"		:	probeIDList,
				"FailureMode"	:	failureList,
		}

	df = pd.DataFrame(data)

	return df