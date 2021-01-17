from gui import menu
import sys
import os
import pandas as pd
import datetime
from pathlib import Path
from datetime import date
from datetime import datetime
from graph import plotGraph
from query import populate
from art import text2art

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y%m%d_%H%M%S")
today = date.today()

def clearscreen():
	os.system("cls")

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

clearscreen()

print(text2art("Probe Replacement", font="small"))
print(text2art("Tracking Tool", font="small"))
print()
print("""
			Developed by     : Idris, Shahidan (11952926)
			Date Developed   : 23 November 2020
			Program          : Probe Replacement Tracking Tool
\n\n""")

WWID = input("WWID: ")
fixID = input("Fixture ID: ")
fixID = fixID.upper()

df = menu()
df = populate(df, fixID)
if 'BRC' in df.columns:
	df['BRC'] = df['BRC'].apply(pd.to_numeric, downcast='signed', errors='ignore')
df['DateTime'] = dateTimeObj

todayyear = datetime.today().year
thisyear = todayyear
nextyear = todayyear + 1
todayday = datetime.today().day
todaymonth = datetime.today().month
lastday = datetime(thisyear, 12, 31).weekday()
lastday = lastday + 1
thisnewyearww = int(datetime(thisyear, 1, 1).strftime("%U"))
newyearday = datetime(nextyear, 1, 1).weekday()
newyearday = newyearday + 1

if lastday == 7:
	lastday = 0

if newyearday == 7:
	workweek = int(datetime(todayyear, todaymonth, todayday).strftime("%U"))
	if thisnewyearww == 0:
		workweek += 1
elif not newyearday == 7:
	if (todaymonth == 12) and (todayday >= (31 - lastday)):
		workweek = 1
	elif (todaymonth == 12) and (todayday < (31 - lastday)):		
		workweek = int(datetime(todayyear, todaymonth, todayday).strftime("%U"))
		if thisnewyearww == 0:
			workweek += 1
	else:
		workweek = int(datetime(todayyear, todaymonth, todayday).strftime("%U"))
		if thisnewyearww == 0:
			workweek += 1

lastday = datetime(thisyear, 12, 31).weekday()
lastday = lastday + 1

todaywwday = datetime.today().weekday()
todaywwday = todaywwday + 1

df['WorkWeek'] = 'WW' + str(workweek) + '.' + str(todaywwday) + "'" + str(todayyear)
df['ReportedBy[WWID]'] = WWID
df['FixtureID'] = fixID

dirStr = os.getcwd() + "\\" + "ProbeReplacement"
dirPath = Path(dirStr)
masterStr = os.getcwd() + "\\" + "ProbeReplacement" + "\\" + "probereplacement_master.csv"
masterPath = Path(masterStr)
prodStr = os.getcwd() + "\\" + "ProbeReplacement" + "\\" + fixID
prodPath = Path(prodStr)
csvStr = os.getcwd() + "\\" + "ProbeReplacement" + "\\" + fixID + "\\" + fixID + ".csv"
csvPath = Path(csvStr)

if not os.path.exists(dirPath):
	os.makedirs(dirPath)

if not os.path.exists(prodPath):
	os.makedirs(prodPath)

parseDates = ['DateTime']

if masterPath.is_file():
	master_df = pd.read_csv(masterPath, parse_dates=parseDates)
	master_df = master_df.append(df, ignore_index=True)
	master_df.to_csv(masterPath, index=False, date_format="%m/%d/%Y %H:%M:%S")
else:
	df.to_csv(masterPath, index=False, date_format="%m/%d/%Y %H:%M:%S")

df = df.drop(columns=['FixtureID'])

if csvPath.is_file():
	product_df = pd.read_csv(csvPath, parse_dates=parseDates)
	product_df = product_df.append(df, ignore_index=True)
	product_df.to_csv(csvPath, index=False, date_format="%m/%d/%Y %H:%M:%S")
else:
	df.to_csv(csvPath, index=False, date_format="%m/%d/%Y %H:%M:%S")

plotGraph(csvPath, fixID)
