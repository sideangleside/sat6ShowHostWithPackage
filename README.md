# sat6ShowHostWithPackage
Script to show which systems have a package (by NVREA)

# Purpose:

Given an NVREA (name,version,release,epoch & arch) of a 
package, show which systems have it installed'

# Requirements

* Red Hat Satellite 6.1 or later
* Python 2.6 or later

# Usage

~~~
./sat6ShowHostWithPackage.py -h
Usage: sat6ShowHostWithPackage.py [options]

Options:
  -h, --help            show this help message and exit
  -l LOGIN, --login=LOGIN
                        Login user
  -p PASSWORD, --password=PASSWORD
                        Password for specified user. Will prompt if omitted
  -s SERVER, --server=SERVER
                        FQDN of sat6 instance
  -n nvrea, --nvrea=nvrea
                        NVREA of the package
~~~


# Example Output

~~~
./sat6ShowHostWithPackage.py -l admin -s satellite.example.com -n bash-4.2.46-12.el7.x86_64
Attempting to connect: https://satellite.example.com/katello/api/systems?per_page=1000
hosts with package bash-4.2.46-12.el7.x86_64 :
dev-node-001.example.com
dev-node-002.example.com
dev-node-005.example.com
dev-node-008.example.com
dev-node-009.example.com
infra-node-001.example.com
infra-node-002.example.com
~~~
