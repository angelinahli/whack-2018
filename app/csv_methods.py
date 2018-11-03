import csv
import random
import datetime
import json

def remember_user(user_id):
	now = datetime.datetime.now()
	user = user_id
	checkin_id = 1
	#if user.has_onboarded = False:
		#initiate onboarding - process in get message of routes.py
	#else:
		#if user.mid_conversation = False:
	with open('checkins.csv', mode='r') as checkin_file:
		for line in checkin_file:
			if user in line:
				checkin_id = checkin_id + 1
		with open('checkins.csv', mode='a') as checkin_file:
			checkin_writer = csv.writer(checkin_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			#checkin_writer.writerow = ["checkin_id","user_id","date_time","baseline","tried_intervention","intervention_id","impact"]
			checkin_writer.writerow([checkin_id, user, now, 4, 5, 6, 7])
			checkin_file.close()
	return True

remember_user(user_id)