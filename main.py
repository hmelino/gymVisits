import datetime
from matplotlib import pyplot as plt
data=open('matusGym.txt').readlines()
errorCount=0
correctCount=0
#data=open('chibiGymData.py').readlines()
#clean data from empty entries and denied acess
db=[v for v in data if len(v)>1 and 'access' not in v.lower()][::-1]

def getDate(s):
	return datetime.datetime.strptime(s[0:19],'%Y-%m-%d %H:%M:%S')

def convertDate(date):
	#convert minutes into percent, 30mins==%50
	minutes=int(int(date.strftime('%M'))*1.666)
	hours=date.strftime('%H')
	return float(f'{hours}.{minutes}')

def debugPrint():
	print('*********************************************************************************************')
	sample=db[iN-8:iN+5]
	print(f'Missing exit from entry of {entry}')
	print(f'Processing now {l}')
	entryString=entry.strftime('%Y-%m-%d')
	entryNexDatString=(entry+datetime.timedelta(1)).strftime('%Y-%m-%d')
	print(f'all same day Data = {[v for v in db if entryString in v]}')
	print(f'all next day Data = {[v for v in db if entryNexDatString in v]}')
	print('**********************************************************************************************')

class Workout():

	def __init__(self):
		self.entry=getDate(db[0])
		self.exit=None
		self.good=0
		self.error=0
		self.workouts=[]
		self.timeOfDay=[]

	def addWorkout(self,wLenght,wTime):
		self.workouts.append(wLenght)
		self.timeOfDay.append(wTime)

	def addEntry(self,entryRaw):
		entry=getDate(entryRaw)
		gap=(entry-self.entry).total_seconds()/60
		if gap>360: #ignore all bathroom/changing room entries
			try:
				workoutLenght=(self.exit-self.entry).total_seconds()/60

				if workoutLenght>200:
					# to fix this

				self.addWorkout(workoutLenght,convertDate(self.entry))
				self.good+=1
				self.exit=None
				self.entry=entry
			except TypeError: #if exit doesnt exists
				self.error+=1
				self.entry=entry

	def addExit(self,exitRaw):
		exit=getDate(exitRaw)
		self.exit=exit

timeOfDayList=[]
workoutLenghtList=[]
entry=getDate(db[0])
exit=None

w=Workout()
for l in db[1:]:
	iN=db.index(l)
	print(iN,l)
	if 'exit' in l:
		w.addExit(l)
	if 'entry' in l:
		w.addEntry(l)



x=w.workouts
y=w.timeOfDay
plt.scatter(x,y,alpha=0.3)
plt.xlim(0,200)
#plt.ylim(0,max(workoutLenghtList)+20)
plt.xlabel('Time of day')
plt.ylabel('Workout lenght (mins)')
plt.grid()
print(f'So far you went to this gym {len(workoutLenghtList)} times')
print(f'Wrong data entries = {errorCount}')
plt.show()
pass