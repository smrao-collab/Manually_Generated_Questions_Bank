#!/bin/bash
cd /home/aziro/Desktop/question_system/Manually_Generated_Questions_Bank
source venv/bin/activate
python3 Automation/daily_l2_js_generator.py >> cron_log_js.txt 2>&1



