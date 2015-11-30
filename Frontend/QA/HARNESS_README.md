Test Harness Readme

Overview : 
This harness accepts a list of tests defined by name in the QA directory as the test file 'testlist'. 
It then walks through the list by name and creates a by parsing the test procedure from the matching file in the subdirectory QA/Tests, 
 All test should be stored as one command line call per line. Once the test commands have been stored internally it will execute them in the order received 
 while logging results. After one test is completed it is removed from memory and no test should have a lifespan greater than it's execution time. 


All test results are stored in the generated log file "TestingLog_yyyy_mm_dd_at_hh_mm", 
comparison failing tests have their returns stored in the QA/FailingTestResults directory for manual examination.
 


 
Once the test has been executed, it's returned results are stored in the temporary file QA/TestResult
 and compared to the known results stored in QA/KnownResults using string literal comparison. Binary comparison would be more efficient, but there's no time.
if comparison fails, this is logged and the test result is stored in FailingTestResults

 
a Test Unit consists of : 
1x command line procedure stored as a text file with the same testname in QA/Tests, 
1x known result stored in text format in QA/KnownResults, it's format should exactly match the command line return you seek.
1x entry in the file testlist corresponding to these two files, with the same name.

 
In the prebundled example : 

Test pullrange grabs a known set of sensor readings from the api and checks to ensure valid range is obtained.


QA/Tests/pullrange contains the single line : curl -u bob:secret "http://smart-irrigation.elasticbeanstalk.com/get_field?table=entry&field=s1&field=s2&start=%222014-10-06_06:27:29%22&end=%222015-12-22_14:04:29%22"


QA/KnownResults/pullrange contains the known return from this call :
[{"s2": 33, "s1": 16, "time": "2014-10-06 06:27:29"}, {"s2": 33, "s1": 16, "time": "2015-10-06 06:27:29"}, {"s2": 57, "s1": 63, "time": "2015-11-02 09:21:05"}, {"s2": 56, "s1": 21, "time": "2015-11-12 12:09:42"}, {"s2": 45, "s1": 26, "time": "2015-11-22 14:04:29"}, {"s2": 41, "s1": 49, "time": "2015-11-30 02:31:02"}, {"s2": 73, "s1": 98, "time": "2015-12-06 19:14:23"}, {"s2": 56, "s1": 37, "time": "2015-12-11 08:47:14"}, {"s2": 15, "s1": 48, "time": "2015-12-14 14:42:38"}, {"s2": 21, "s1": 99, "time": "2015-12-21 07:13:15"}]


QA/testlist has the appropriate entry 'pullrange' on line 1.
 

 
Note that due to the shell usage in the harness, you can farm tests out to supplemental scripts. 
for example:


You could write a test called 'pythontest' whose contents are stored in a python script 'test.py'
you could then add the call 'python <dir>/test.py' on line of 'pythontest' in the QA/Tests directory
you could write the known ttyl results in 'pythontest' in QA/KnownResults


once adding pythontest to testlist, this would fire off the python script as a subprocess and should confirm the results, (I haven't tested this specific process in a wide range of cases, so let me know if you choose to do this and encounter difficulty)