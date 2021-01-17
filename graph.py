import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os
from pathlib import Path
from collections import Counter

def plotGraph(filename, fixtureID):

	today = date.today()

	dirStr = os.getcwd() + "\\" + "ProbeReplacement" + "\\" + "plots" + "\\" + fixtureID
	dirPath = Path(dirStr)

	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

	df = pd.read_csv(filename)

	probeID = df['ProbeID'].tolist()
	failureMode = df['FailureMode'].tolist()

	a = dict(Counter(probeID))
	b = dict(Counter(failureMode))

	plt.figure(1)
	plt.subplot(211)
	plt.title("Top Probe ID Replacement Count")
	plt.ylabel("Quantity")
	plt.bar(range(len(a)), list(a.values()), align='center')
	plt.xticks(range(len(a)), list(a.keys()))
	plt.subplot(212)
	plt.title("Top Failure Mode Causing Replacement Count")
	plt.ylabel("Quantity")
	plt.bar(range(len(b)), list(b.values()), align='center')
	plt.xticks(range(len(b)), list(b.keys()))

	fig = plt.gcf()

	fig.canvas.set_window_title('Bar Chart for Probe ID and Failure Mode Counts')

	fig.set_size_inches(12.8, 8)

	plt.savefig(dirStr + "\\" + str(today) + ".pdf", dpi=300)

	while True:
		plt.show(block=False)
		i = input("\n\nEnter text or Enter to quit... ")
		if not i:
			break