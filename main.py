import datetime
from matplotlib import pyplot as plt
data=open('matusGym.txt').readlines()
errorCount=0
correctCount=0
#clean data from empty entries and denied acess
db=[v for v in data if len(v)>1 and 'access' not in v.lower()][::-1]

def getDate(s):
	return datetime.datetime.strptime(s[0:19],'%Y-%m-%d %H:%M:%S')

def convertDate(date):
	#convert minutes into percent, 30mins==50
	minutes=int(int(date.strftime('%M'))*1.666)
	hours=date.strftime('%H')
	return float(f'{hours}.{minutes}')


class Workout():

	def __init__(self):
		self.entry=getDate(db[0])
		self.exit=None
		self.good=0
		self.error=0
		self.workouts=[]
		self.timeOfDay=[]
		self.lastAdded=self.entry
		self.lastAddedIsEntry=True
		
	def processWorkout(self,date):
		if self.entry and self.exit:
			workoutTime=(self.exit-self.entry).total_seconds()/60
			
			self.workouts.append(workoutTime)
			self.timeOfDay.append(convertDate(date))
			self.good+=1
			self.discartData()
		else:
			self.error+=1
			
	def discartData(self):
		self.entry,self.exit=None,None
		
	def removeWrongWorkouts(self):
		#counts average and remove off average data
		averageWorkoutLimit=(sum(self.workouts)/len(self.workouts))*4
		cleanedWorkouts=[]
		for w in self.workouts:
			iN=self.workouts.index(w)
			if w < averageWorkoutLimit:
				cleanedWorkouts.append(w)
			else:
				self.timeOfDay.pop(iN)
		self.workouts=cleanedWorkouts
			
	def processIt(self,data):
		date=getDate(data)
		gap=(date-self.lastAdded).total_seconds()/60
		if gap>360:
			self.processWorkout(date)
			if 'entry' in data:
				self.entry=date
		if 'exit' in data:
			self.exit=date
		self.lastAdded=date

w=Workout()
for l in db[1:]:
	print(l)
	w.processIt(l)
w.removeWrongWorkouts()

x=w.timeOfDay
y=w.workouts
plt.scatter(x,y,alpha=0.3)
plt.xlim(0,24)
plt.ylim(0,max(w.workouts)+20)
plt.xlabel('Time of day')
plt.ylabel('Workout lenght (mins)')
plt.grid()
print(f'So far you went to this gym {len(w.workouts)+w.error} times')
print(f'Corrupted data count = {w.error} ')
plt.show()
pass
