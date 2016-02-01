#!/usr/bin/env python

# File: sat6ShowHostWithPackage.py
# Author: Rich Jerrido <rjerrido@outsidaz.org>
# Purpose: given an NVREA (name,version,release,epoch & arch) of a 
#          package, show me which systems have it installed'
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import getpass
import urllib2
import base64
import sys
import ssl
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user", metavar="LOGIN")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD")
parser.add_option("-s", "--server", dest="server", help="FQDN of sat6 instance", metavar="SERVER")
parser.add_option("-n", "--nvrea", dest="nvrea", help="NVREA of the package", metavar="nvrea")
(options, args) = parser.parse_args()

if not ( options.login and options.server and options.nvrea ):
	print "Must specify a login, server and nvrea (will prompt for password if omitted).  See usage:"
	parser.print_help()
	print "\nExample usage: ./sat6ShowHostWithPackage.py -l admin -p sat6.example.com -n abrt-addon-ccpp-2.0.8-26.el6.x86_64"
	sys.exit(1)
else:
	login = options.login
	password = options.password
	server = options.server
	nvrea = options.nvrea

if not password: password = getpass.getpass("%s's password:" % login)


if hasattr(ssl, '_create_unverified_context'):
	    ssl._create_default_https_context = ssl._create_unverified_context

#### Get the list of hosts
url = "https://" + server + "/katello/api/systems?per_page=1000"
try:
 	request = urllib2.Request(url)
	print "Attempting to connect: " + url
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

hostdata = json.load(result)
print "hosts with package %s :" % (nvrea)
for host in hostdata['results']:
	detailedurl = "https://" + server + "/katello/api/systems/" + host["uuid"] + "/packages/"
	try:
		sysinfo = urllib2.Request(detailedurl)
		base64string = base64.encodestring('%s:%s' % (login, password)).strip()
		sysinfo.add_header("Authorization", "Basic %s" % base64string)
		sysresult = urllib2.urlopen(sysinfo)
		packagedata = json.load(sysresult)
		if packagedata.has_key("errors"):
			print packagedata["errors"]
		if packagedata["results"]:
			for package in packagedata['results']:
				if package["nvrea"] == nvrea:
					print host["name"]
	except urllib2.HTTPError as e:
		if str(e) != "HTTP Error 400: Bad Request":
			raise
			sys.exit(2)

sys.exit(0)
