
# finding_available_people


This simple script searches text files in the directory which we adding as argument. 
Then it tries to find available people. There are dates in the files when the person is busy. 
Date alone without time means that person is busy whole day. 
Script prints first suitable to arguments people. 
Script accept a named parameters: --calendars - name of directory in which to search file .txt 
                                  --duration - following in minutes e.g. 
                                  --duration 30 means 30 minuts --minimum_people - number of people to be matched
                                  

## example


assuming it's 2030-01-02 10:00:00 now and
    /simple/alex.txt consists of: 
	2030-01-02 13:15:00 - 2030-01-02 13:59:59
    /simple/brian.txt consists of: 
    	2030-01-01
	2030-01-02 00:00:00 - 2030-01-02 12:59:59
Calling the script: 
python find-available-slot.py --calendars=simple --duration=30 --minimum_people=2 OR 
python find-available-slot.py --calendars simple --duration 30 --minimum_people 2 OR 
python find-available-slot.py - because any argument has default value

It print: 2030-01-02 14:00
