from subprocess import Popen, PIPE
import shutil
import time
import datetime
import sys

logFileName = 'gitWatch.log'
datetimeFormat = '%Y-%m-%d %H:%M:%S'
def callProcess(cmd):
	p = Popen(cmd, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()	
	return stdout.decode('utf-8', 'replace')

def report(filename, date = None):
	print('report ' + filename)
	with open(filename) as f:
		lines = f.readlines()
		lastBranch = ''
		startDate = None
		timeSpan = None
		lastLine = lines[-1]
		for l in lines:
			splitted = l.split('\t')
			dateTimeStr =splitted[0]
			branch = splitted[1]
			if lastBranch != branch or l == lastLine:
				endDate = datetime.datetime.strptime(dateTimeStr, datetimeFormat)
				if startDate != None:
					timeSpan = endDate - startDate
					print (dateTimeStr, lastBranch, timeSpan)
				lastBranch = branch
				startDate = endDate

def getLogLine(content):
	now = datetime.datetime.now().strftime(datetimeFormat)
	logLine = '%s\t%s' % (now, content)
	return logLine
				
arglen = len(sys.argv)
if arglen > 1:
	filename = sys.argv[1]
	if arglen > 2:
		date = sys.argv[2]
	else:
		date = None
	report(filename, date)
	exit()
	
lastBranch = ''
try:
	while True:
		result = callProcess('git status -b --porcelain')
		firstLine = result.split('\n')[0]
		branch = firstLine.split(' ')[1]
		logLine = getLogLine(branch)
		print (logLine)
		
		log = open(logFileName, 'a')
		print (logLine, file=log)
		log.close()		
		time.sleep(60)
except (KeyboardInterrupt, SystemExit):
	logLine = getLogLine('end')
	print (logLine)
	log = open(logFileName, 'a')
	print (logLine, file=log)
	log.close()

