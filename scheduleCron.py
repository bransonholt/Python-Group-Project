#!/bin/env python3
#
# Automation portion of program
# author: Branson Holt
# version: 12/03/18
#
from crontab import CronTab
 
my_cron = CronTab(user='Holt')
job = my_cron.new(command='/usr/local/bin/python3 /Users/Holt/automate.py')
job.minute.every(1)
 
my_cron.write()
for job in my_cron:
    print(job)

