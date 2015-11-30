import datetime
import subprocess
import os.path
import sys

class TestHarness :
	date =  None
	tests = None
	test = None
	
	def __init__(self) :
		thisDate = datetime.datetime.now()
		self.date = thisDate.strftime('%Y-%m-%d_at_%H_%M')
		#initialize new log 
		logstream = open("TestingLog_" + self.date, "w")
		logstream.close()
	
	def accumulateTests(self):
		with open("testlist", "r") as fstream :
			self.tests = fstream.read().splitlines()
		
		if len(self.tests) == 0:
			print "Harness Error : No tests detected during accumulateTests"
			sys.exit(1)
	
	def setupTest(self):
		self.test = Test(self.tests.pop(0))
		self.logLine("Setting Up Test : " + self.test.name)
		self.test.stageTest()
		
	def runTest(self):
		self.logLine("Executing Up Test : " + self.test.name)
		self.test.executeTest()
		self.logLine("Performing Comparison")
		self.test.compareResults()
		
		result = "SUCCEEDED" if not self.test.hasFailed else "FAILED"
		self.logLine("Test : " + self.test.name + " has  " + result)
		
	def teardownTest(self):
		self.Test = None
		self.logLine("--------------------------------")
		
	def logLine(self, info):
		thisDate = datetime.datetime.now()
		timestamp = thisDate.strftime('<%H:%M:%S>')
		
		with open("TestingLog_" + self.date, "a") as lstream:
			lstream.write(timestamp + " : " + info + "\n")
		
		
class Test :
	def __init__(self, testName):
		thisDate = datetime.datetime.now()
		self.datePerformed = thisDate.strftime('%Y-%m-%d_at_%H_%M')
		self.hasFailed = False
		self.cmds = []
		self.name = testName
	
	def stageTest(self) :
		testFile = None
		try :
			#ensure platform independence
			testFile = open( os.path.normpath("Tests/" + self.name) )
			self.cmds = testFile.readlines()
		except IOError as error:
			self.reportFailure(error, "staging")
			return
	
	def executeTest(self):
		
		while self.cmds and self.hasFailed is False:
			print self.cmds
			try :
				testResults = subprocess.check_output(self.cmds.pop(0), shell=True)
				
				#kept separate to ensure stream closure in exception, although I'm sure python probably does this.
				file = open('TestResult', "w")
				file.write(testResults)
				file.close()
				
			except subprocess.CalledProcessError as error:
				self.reportFailure(error, "execution")
				return				
	
	def compareResults(self):
		#get stripped results
		fileStream = open( os.path.normpath("KnownResults/" + self.name), "r")
		knownResults = fileStream.read().splitlines()
		fileStream.close()
		fileStream = open( "TestResult", "r")
		theseResults = fileStream.read().splitlines()
		fileStream.close()
		
		
		#quick short circuit to save time in trivial reject cases
		if len(knownResults) != len(theseResults) :
			self.reportFailure(None, "result comparison (Result Cardinality Differs)")
			return
			
		for index in range(len(knownResults)) :
			if (knownResults[index] != theseResults[index]) :
				self.reportFailure( None, "result comparison failed at line {0}".format(index+1))
				storedResults = open( os.path.normpath("FailingTestResults/" + self.name+"_Failure_" + self.datePerformed), "w" )
				storedResults.writelines(theseResults)
				return
		
		print ("Test: " + self.name + ", has succeeded with no flaws.")

	def reportFailure(self, error, stage) :
		print "Test: " + self.name + ", has failed.\n"
		print "Observed Error : "
		print error.output+"\n" if hasattr(error, "output") else "Test File Not Found or output not supplied\n"
		print "Return Code : "
		print str(error.returncode)+"\n" if hasattr(error, "returncode") else "Not Supplied\n"
		print "Failure occurred during " + stage +"\n--------------------------------\n"
		self.hasFailed = True
		
harness = TestHarness()
harness.accumulateTests()

harness.logLine("Beginning Testing Process")
harness.logLine("--------------------------------")
while harness.tests :
	harness.setupTest()
	harness.runTest()
	harness.teardownTest()

harness.logLine("Testing Completed")
