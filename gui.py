import PySimpleGUI as sg
from table import makeTable, deleteOneEntry, deleteAllEntries, storeTable
from failure_parser import parseList

def menu():
	probeID = []
	failureMode = []

	sg.theme('Reddit')   # Add a touch of color
	# All the stuff inside your window.
	layout = [  [sg.Text('Probe ID:'), sg.InputText()],
				[sg.Text('Failure Mode:'), sg.Combo(parseList())],
	            [sg.Button('Add Input'), sg.Button('Delete One Entry'), sg.Button('Delete All Entries'), sg.Button('Close Window')] ]

	# Create the Window
	window = sg.Window('ICT Fixture Probe Replacement Tracker', layout)
	# Event Loop to process "events" and get the "values" of the inputs
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Close Window': # if user closes window or clicks cancel
			break
		if event == 'Delete One Entry':
			deleteOneEntry(probeID, failureMode)
		if event == 'Delete All Entries':
			deleteAllEntries(probeID, failureMode)
		if event == 'Add Input':
			probeID.append(values[0].upper())
			failureMode.append(values[1])

		makeTable(probeID, failureMode)

	window.close()

	return storeTable(probeID, failureMode)