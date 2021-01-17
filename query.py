import pandas as pd
import xlrd
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from time import sleep
from sys import exit

def clearscreen():
	os.system("cls")

def handleString(colName):

	colName = colName.strip()
	colName = colName.lower()
	colName = colName.replace(" ", "")
	colName = colName.replace("_", "")
	colName = colName.replace("/", "")
	colName = colName.replace("#", "")

	return colName

def populate(dataframe, fixtureID):
	pathStr = os.getcwd() + "\\" + "ProbeList"
	pathObj = Path(pathStr)
	
	probeID_list = []
	netName_list = []
	probeSize_list = []
	brc_list = []
	probePartNumb_list = []
	loc_list = []
	text_list = []
	xy_list = []

	my_netname = []
	my_probesize = []
	my_brc = []
	my_partnum = []
	my_loc = []
	my_xy = []

	probeFiles = [f for f in listdir(pathObj) if isfile(join(pathObj, f))]

	for items in probeFiles:
		if items.startswith(fixtureID):
			fullPath = pathObj / items
			print("\nFound ProbeList... ", items)
			workbook = xlrd.open_workbook(fullPath, encoding_override="cp1252")
			worksheet = workbook.sheet_by_index(0)

			i = 1
			j = 0
			done_tag = 0
			rows = worksheet.nrows - 1
			cols = worksheet.ncols - 1

			while True:
				columnName = worksheet.cell(0, j).value
				
				i = 1
				if (handleString(columnName) == "probeid") or ((handleString(columnName) == "probe") and (str(worksheet.cell(1, j).value).startswith("P") or str(worksheet.cell(1, j).value).startswith("p"))):
					print("\nReading Probe ID...")
					while True:
						probeID_list.append(worksheet.cell(i, j).value)
						if i == rows:
							break
						i = i + 1

				i = 1
				if (handleString(columnName) == "netname") or (handleString(columnName) == "nodename") or (handleString(columnName) == "node") or (handleString(columnName) == "net"):
					print("\nReading Net Name...")
					while True:
						netName_list.append(worksheet.cell(i, j).value)
						if i == rows:
							break
						i = i + 1

				i = 1
				if handleString(columnName) == "probesize":
					print("\nReading Probe Size...")
					while True:
						probeSize_list.append(worksheet.cell(i, j).value)
						if i == rows:
							break
						i = i + 1

				i = 1
				if (handleString(columnName) == "brc") or (handleString(columnName) == "brcc"):
					print("\nReading BRC...")
					while True:
						temp = str(worksheet.cell(i, j).value)
						temp = temp.replace(",", "")
						brc_list.append(temp)
						if i == rows:
							break
						i = i + 1

				i = 1
				if handleString(columnName) == "probepn":
					print("\nReading Probe Part Number...")
					while True:
						probePartNumb_list.append(worksheet.cell(i, j).value)
						if i == rows:
							break
						i = i + 1

				i = 1
				if ((handleString(columnName) == "loc") or (handleString(columnName) == "topbottom") or (handleString(columnName) == "location")) and (done_tag == 0):
					print("\nReading Probe Location...")
					done_tag = 1
					while True:
						dummy = worksheet.cell(i, j).value
						dummy = str(dummy).replace("(", "")
						dummy = dummy.replace(")", "")
						if len(dummy) > 1:
							dummy = dummy[:1]
						loc_list.append(dummy)
						if i == rows:
							break
						i = i + 1

				i = 1
				if handleString(columnName) == "x":
					while True:
						text = "X" + str(worksheet.cell(i, j).value)
						text_list.append(text)
						if i == rows:
							break
						i = i + 1

				i = 1
				if handleString(columnName) == "y":
					while True:
						for things in text_list:
							things = things + "Y" + str(worksheet.cell(i, j).value)
						xy_list.append(things)
						if i == rows:
							break
						i = i + 1

				i = 1
				if handleString(columnName) == "xy":
					print("\nReading Probe Coordinates (XY)...")
					while True:
						xy_list.append(worksheet.cell(i, j).value)
						if i == rows:
							break
						i = i + 1

				if j == cols:
					break

				j = j + 1

			# TODO: Process the lists to display database
			probeID_df = dataframe['ProbeID'].values.tolist()
			
			clearscreen()

			print("\nMatching input probe details with probe list...\n")

			for prbs in probeID_df:
				for probes in probeID_list:
					if handleString(probes) == handleString(prbs):
						sleep(2)
						print("Found matching ProbeID:", probes)
						val = probeID_list.index(probes)
						my_netname.append(netName_list[val])
						print("Net Name:", netName_list[val])
						my_probesize.append(probeSize_list[val])
						print("Probe Size:", probeSize_list[val])
						my_brc.append(brc_list[val])
						print("BRC:", brc_list[val])
						my_partnum.append(probePartNumb_list[val])
						print("Part Number:", probePartNumb_list[val])
						my_loc.append(loc_list[val])
						print("Location:", loc_list[val])
						my_xy.append(xy_list[val])
						print("XY-Coordinates:", xy_list[val])
						print()
						sleep(2)

			if my_netname:
				dataframe["NetName"] = my_netname
			elif not my_netname:
				dataframe["NetName"] = ""

			if my_probesize:
				dataframe["ProbeSize"] = my_probesize
			elif not my_probesize:
				dataframe["ProbeSize"] = ""

			if my_brc:
				dataframe["BRC"] = my_brc
			elif not my_brc:
				dataframe["BRC"] = ""

			if my_partnum:
				dataframe["PartNumber"] = my_partnum
			elif not my_partnum:
				dataframe["PartNumber"] = ""

			if my_loc:
				dataframe["Location"] = my_loc
			elif not my_loc:
				dataframe["Location"] = ""

			if my_xy:
				dataframe["XY"] = my_xy
			elif not my_xy:
				dataframe["XY"] = ""

	return dataframe