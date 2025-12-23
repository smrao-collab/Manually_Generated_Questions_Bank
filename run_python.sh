#!/bin/bash
cd /home/aziro/Desktop/question_system/Manually_Generated_Questions_Bank
source venv/bin/activate
python3 Automation/daily_l2_python_easy_generator.py >> cron_log_python.txt 2>&1


