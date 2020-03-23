import datetime
from matplotlib import pyplot as plt
data=open('gymsData.py').readlines()
#data=open('chibiGymData.py').readlines()
db=[v for v in data if len(v)>1][::-1]

def getDate(s):
	return datetime.datetime.strptime(s[0:19],'%Y-%m-%d %H:%M:%S')

def convertDate(date):
	#convert minutes into percent, 30mins==%50
	minutes=int(int(date.strftime('%M'))*1.666)
	hours=date.strftime('%H')
	return float(f'{hours}.{minutes}')


timeList=[]
lenght=[]

entry=getDate(db[0])
exit=None


for d in db[1:]:
	if 'No access' in d:
		pass
	else:
		if 'exit' in d:
			exit=getDate(d)
		if 'entry' in d:
			newEntry=getDate(d)
			timeDifference=(newEntry-entry).total_seconds()
			if timeDifference>14400:
				spendInGym=round((exit-entry).seconds/60,2)
				lenght.append(spendInGym)
				print(spendInGym)
				timeOfDay=convertDate(entry)
				timeList.append(timeOfDay)
				
				if spendInGym>1200:
					errorIndex=db.index(d)
					print(db[errorIndex-8:errorIndex])
					print(f'  door entry {entry}')
					print(f'  exit {exit}')
				entry=newEntry
				
			
plt.scatter(timeList,lenght,alpha=0.3)
#plt.ylim(0,250)
plt.xlim(0,24)
plt.xlabel('Time of day')
plt.ylabel('Workout lenght (mins)')
plt.grid()
plt.show()	

#23.78 2018-06-14 23:47:45 2018-06-19 21:52:24
