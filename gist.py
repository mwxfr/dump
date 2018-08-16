import json
import re


def sorted_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# Load the results of the current scan
with open('scan.json', 'r') as f:
    data = json.load(f)

# Look for all errors that are specific to this change
hosts = []
for host in data[0]['data']:
	name = host['host']
	rank = host['rank']
	error = host['response']['result']['info']['status']
	if error == 2153398259:
	    hosts.append('%s,%s' % (rank, name))

# Create an object that indexes these hosts by rank number
sorted_hosts = sorted_nicely(hosts)
indexed_hosts = {}
for item in sorted_hosts:
	index = item.split(',')[0]
	indexed_hosts[index] = item.split(',')[1]

# Load the non-expired host list from the previous run.
# We will just use it for its cert expiration data, since
# the current data set didn't get its own.
indexed_master = {}
with open('prev_master_hosts.txt', 'r') as f:
	for line in f:
		temp = line.split(',')[0]
		indexed_master[temp] = line.strip()

# Pick out the entries of the master list using the hosts
# from this run.
master_hosts = []
for host in indexed_hosts:
	try:
	    master_hosts.append(indexed_master[host])
	except:
	    pass

# Print out the current error hosts
all_hosts = open('ranked_hosts.txt', 'w')
for item in sorted_hosts:
    all_hosts.write(item + '\n')
all_hosts.close()

# Print out the current error hosts with cert expiration data
final_list = sorted_nicely(master_hosts)
non_expired_hosts = open('non_expired_hosts.txt', 'w')
for item in final_list:
    non_expired_hosts.write(item + '\n')
non_expired_hosts.close()
