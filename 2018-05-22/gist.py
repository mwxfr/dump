import json
import re


def natural_sort( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

log_file = '2018-05-22.json'
expiration_date = 1539691199000000 # 2018-10-16 11:59:59

all_hosts = []
non_expired_hosts = []
problem_hosts = []

with open(log_file) as json_data:
    d = json.load(json_data)
    hosts = d[0]['data']
    for host in hosts:
    	rank = '%s' % host['rank']
    	all_hosts.append(rank + ', ' + host['host'])
        try:
	    	validity = host['response']['result']['info']['ssl_status']['serverCert']['validity']
	    	not_after = validity['notAfter']
	        if not_after > expiration_date:
	        	non_expired_hosts.append(rank + ', ' + host['host'] + ', ' + validity['notAfterGMT'])
        except:
            problem_hosts.append(host['host'])
        	
print 'Excluding %s problem hosts that failed for reasons other than certificate.' % len(problem_hosts)

print 'Writing file \'ranked_hosts.txt\' to disk.'
sorted_hosts = natural_sort(all_hosts)
with open('ranked_hosts.txt', 'a') as output:
    for host in sorted_hosts:
        output.write('%s\n' % host)

print 'Writing file \'non_expired_hosts.txt\' to disk.'
sorted_non_expired_hosts = natural_sort(non_expired_hosts)
with open('non_expired_hosts.txt', 'a') as output:
    for host in sorted_non_expired_hosts:
        output.write('%s\n' % host)
