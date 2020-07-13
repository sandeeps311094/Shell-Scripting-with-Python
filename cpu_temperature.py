#----  This program makes use of the acpi command of Bash to get the fan speed and CPU temperature. Depending on what the temperature is, it displays the temperature in a specefic color. It then writes the fan speed and twmperature values into a database. A method also loads them into a pandas dataframe.


import os
import subprocess
import imp
from nltk import word_tokenize
import re
import time
import mysql.connector as sqlc
import pandas as pd

def calc_values():
	sl_no = 1
	iterator = 1
	while (iterator <= 30):
		time.sleep (2.05)
		str1 = subprocess.getoutput ("sensors")
		ls = word_tokenize (str1)


		i = 0
		RPM = 0 ; cpu_temp = 0
		inti = ''
		while (i < len (ls)):
			if (ls [i] == 'Fan'):
				RPM = ls[i + 2]
			if (ls [i] == 'CPU'):
				cpu_temp = ls[i + 2]

			i += 1

		for i in cpu_temp:
			if ((ord (i) in range (48, 58)) or (ord (i) == 46)):
				inti = inti + i
		floater = float (inti)

		if (floater > 50):
			os.system ('clear')
			print ("\n----------------------------")
			if (RPM == '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |OFF|\nCPU temperature --> \033[0;31m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

			elif (RPM != '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |ON|\nCPU temperature --> \033[0;31m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

		#--

		elif (floater > 45 and floater <= 50):
			os.system ('clear')
			print ("\n----------------------------")
			if (RPM == '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |OFF|\nCPU temperature --> \033[0;33m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

			elif (RPM != '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |ON|\nCPU temperature --> \033[0;33m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")
		#--

		elif (floater > 40 and floater <= 45):
			os.system ('clear')
			print ("\n----------------------------")
			if (RPM == '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |OFF|\nCPU temperature --> \033[0;32m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

			elif (RPM != '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |ON|\nCPU temperature --> \033[0;32m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")
		#--

		elif (floater <= 40):
			os.system ('clear')
			print ("\n----------------------------")
			if (RPM == '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |OFF|\nCPU temperature --> \033[0;34m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

			elif (RPM != '0'):
				print ("Fan speed --> \033[0;37m{}\033[0m rpm |ON|\nCPU temperature --> \033[0;34m{}\033[0m".format (RPM, cpu_temp))
				print ("----------------------------\n")

		load_to_dbase (sl_no, RPM, floater)
		sl_no += 1
		iterator += 1

	db_to_dframe()
#------------

def load_to_dbase (sl_no, RPM, cpu_temp):
		RPM = int (RPM)

		if (int (cpu_temp > 50)):
			level = 'VERY HIGH'
		elif (int (cpu_temp) > 45 and int (cpu_temp) <= 50):
			level = 'HIGH'
		elif (int (cpu_temp) > 40 and int (cpu_temp) <= 45):
			level = 'NORMAL'
		elif (int (cpu_temp) <= 40):
			level = 'COLD'
		else:
			level = 'INVALID'

		ls = [str (sl_no), str (RPM), str (cpu_temp), str (level)]
		print ("LS --> {}".format (ls))

		db = sqlc.connect (
				host = "localhost",
				user = "san",
				passwd = "san123",
				database = "CPU"
		)

		cursor = db.cursor()
		command = "INSERT INTO cpu_stats (Sl_no, Fan_speed, Temperature, Level) VALUES (%s, %s, %s, %s)"

		cursor.execute (command, ls)
		db.commit()

		cursor.execute ("SELECT * FROM cpu_stats")
		result = cursor.fetchall()

#------------

def db_to_dframe():
	db = sqlc.connect (
		host = "localhost",
		user = "san",
		passwd = "san123",
		database = "CPU"
	)

	ls_db = []
	cursor = db.cursor()
	cursor.execute ("SELECT * FROM cpu_stats")
	result = cursor.fetchall()

	for i in result:
		ls_db.append (i)

	dframe = pd.DataFrame (ls_db)


	dframe ['Sl no'] = dframe [0]
	dframe ['Fan speed'] = dframe [1]
	dframe ['CPU Temperature'] = dframe [2]
	dframe ['Level'] = dframe [3]

	del dframe [0] ; del dframe [1] ; del dframe [2] ; del dframe [3]


	print (dframe)

#------------

calc_values()
#db_to_dframe()
