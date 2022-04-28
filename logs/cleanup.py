import sys

def cleanup_access_log(ip='208.115.199.26'):
	new_lines = []
	with open('access.log', 'r') as f:
		for line in f.readlines():
			if ip in line:
				pass
			else:
				new_lines.append(line)
	with open('clean.access.log', 'a') as f:
		print("Saving to clean.access.log")
		f.writelines(new_lines)

if len(sys.argv) > 1:
	print(f" Cleaning access.log file from all IPs that are {sys.argv[1]} ")
	cleanup_access_log(sys.argv[1])
else:
	print("Cleaning access.log file from all IPs that are 208.115.199.26 (uptimerobot)")
	cleanup_access_log()