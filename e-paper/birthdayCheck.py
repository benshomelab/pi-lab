from datetime import *
import csv

def importBdays():
	imported_bdays = []
	with open('<path to birthdays.txt file>', 'r') as bdays:
		reader = csv.reader(bdays)
		for row in reader:
			imported_bdays.append(row)
	return imported_bdays

def birthdaysSoon():
	bdaysToExport = []
	bdays = importBdays()
	lookOutToDate = datetime.today() + timedelta(days=31)
	bdays = sortBdays(bdays)
	for person in bdays:
		thisYear = datetime.strptime(person[1] + "/" + str(date.today().year), "%m/%d/%Y")
		nextYear = datetime.strptime(person[1] + "/" + str(date.today().year + 1), "%m/%d/%Y")
		if(datetime.strptime(datetime.today().strftime("%m/%d/%Y, 00:00:00"),"%m/%d/%Y, %H:%M:%S") <= thisYear <= lookOutToDate):
			bdaysToExport.append(person[0] + " - " + person[1])
		elif(datetime.strptime(datetime.today().strftime("%m/%d/%Y, 00:00:00"),"%m/%d/%Y, %H:%M:%S") <= nextYear <= lookOutToDate):
			bdaysToExport.append(person[0] + " - " + person[1])
	print(str(isSorted(bdays)))
	return bdaysToExport

# Sorting bdays based on date
def sortBdays(bdays):
	holder = None
	while(isSorted(bdays) == False):
		for index, person in enumerate(bdays):
			if(index < len(bdays)-1):
				# Check if daysfromnow of current person is greater than the daysfromnonw for the next person
				if(daysFromNow(bdays[index]) > daysFromNow(bdays[index+1])):
					# If out of order, then swap
					#print('swapping')
					holder = bdays[index]
					bdays[index] = bdays[index+1]
					bdays[index+1] = holder
	#print('sorted')
	return bdays

# Check if sorted
def isSorted(bdays):
	for index, person in enumerate(bdays):
		if(index < len(bdays)-2):
			if(daysFromNow(person) > daysFromNow(bdays[index+1])):
				return False
	return True

# return int # of days until bday
def daysFromNow(person):
	today = datetime.strptime(datetime.today().strftime("%m/%d/%Y, 00:00:00"),"%m/%d/%Y, %H:%M:%S")
	# holders for both this year and next year
	thisYear = datetime.strptime(person[1] + "/" + str(date.today().year), "%m/%d/%Y")
	nextYear = datetime.strptime(person[1] + "/" + str(date.today().year + 1), "%m/%d/%Y")
	# calculating how many days until both
	thisYear = thisYear - today
	nextYear = nextYear - today
	if(thisYear.days < 0):
		return nextYear.days
	else:
		return thisYear.days
