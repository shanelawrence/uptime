import os
import sys
import socket
import datetime
import time


FILE = os.path.join(os.getcwd(), "networkinfo.log")
# create log file in the currenty directory

def ping():
	# open a connection with the defined IP and port
    # note it is NOT an ICMP echo, 'ping'
    # but actually opens a connection
	try:
		socket.setdefaulttimeout(3)
		
		# if data interruption occurs for 3 seconds, <except> part will be executed
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# AF_INET: address family
		# SOCK_STREAM: type for TCP
		host = "8.8.8.8" 
        # Google DNS
        # host = "75.75.75.75"
        # Comcast DNS
		port = 53
        

		server_address = (host, port)
		s.connect(server_address)

	except OSError as error:
		return False
		# function returns false after data interruption

	else:
		s.close()
		# close connection after the ping is complete
        # very important to not DOS the server
		return True


def calculate_time(start, stop):

	# calculate down time and convert to seconds
	difference = stop - start
	seconds = float(str(difference.total_seconds()))
	return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def first_check():
	# check if the system was already connected

	if ping():
		# if ping returns true
		live = "\nCONNECTION ACQUIRED\n"
		print(live)
		connection_acquired_time = datetime.datetime.now()
		acquiring_message = "connection acquired at: " + \
			str(connection_acquired_time).split(".")[0]
		print(acquiring_message)

		with open(FILE, "a") as file:
		
			# writes into the log file
			file.write(live)
			file.write(acquiring_message)

		return True

	else:
		# if ping returns false
		not_live = "\nCONNECTION NOT ACQUIRED\n"
		print(not_live)

		with open(FILE, "a") as file:
		
			# writes into the log file
			file.write(not_live)
		return False


def main():

	monitor_start_time = datetime.datetime.now()
	monitoring_date_time = "monitoring started at: " + \
		str(monitor_start_time).split(".")[0]

	if first_check():
		# if true
		print(monitoring_date_time)
		# monitoring will only start once a connection has been established

	else:
		# if false
		while True:
		
			# infinite loop to see if the connection is acquired
			if not ping():
				
				# if connection not acquired
				time.sleep(1)
			else:
				
				# if connection is acquired
				first_check()
				print(monitoring_date_time)
				break

	with open(FILE, "a") as file:
	
		# create the file if it does not exist
		# write into the file networkinfo.log,
		# "a" - append: opens file for appending,
		file.write("\n")
		file.write(monitoring_date_time + "\n")

	while True:
	
		# monitoring, infinite loop
		if ping():
			
			# if true: the loop will execute every 5 seconds
			time.sleep(5)

		else:
			# if false: fail message will be displayed
			down_time = datetime.datetime.now()
			fail_msg = "disconnected at: " + str(down_time).split(".")[0]
			print(fail_msg)

			with open(FILE, "a") as file:
				# writes into the log file
				file.write(fail_msg + "\n")

			while not ping():
			
				# infinite loop, will run untill ping() returns true
				time.sleep(1)

			up_time = datetime.datetime.now()
			
			# after loop breaks, connection restored
			uptime_message = "connected again: " + str(up_time).split(".")[0]

			down_time = calculate_time(down_time, up_time)
			unavailablity_time = "connection was unavailable for: " + down_time

			print(uptime_message)
			print(unavailablity_time)

			with open(FILE, "a") as file:
				
				# log entry for connection restored time, and down time
				file.write(uptime_message + "\n")
				file.write(unavailablity_time + "\n")

main()
