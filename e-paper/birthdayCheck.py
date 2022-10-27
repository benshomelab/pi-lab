from datetime import *
import csv

def importBdays():
	imported_bdays = []
	with open('<your path to txt file containing bdays>', 'r') as bdays:
		reader = csv.reader(bdays)
		for row in reader:
			imported_bdays.append(row)
	return imported_bdays

def birthdaysSoon():
	bdaysToExport = []
	bdays = importBdays()
	lookOutToDate = datetime.today() + timedelta(days=31)
	for person in bdays:
		thisYear = datetime.strptime(person[1] + "/" + str(date.today().year), "%m/%d/%Y")
		nextYear = datetime.strptime(person[1] + "/" + str(date.today().year + 1), "%m/%d/%Y")
		if(datetime.today() <= thisYear <= lookOutToDate):
			bdaysToExport.append(person[0] + " - " + person[1])
		elif(datetime.today() <= nextYear <= lookOutToDate):
			bdaysToExport.append(person[0] + " - " + person[1])
	return bdaysToExport