#!/bin/bash

python3 stats.py -u farr/users-merged.txt -n farr/nodes.old -b "2013-01-01 00:00:01" -e "2017-01-01 00:00:00" -p oldfarr_farrnodes -d sgelogs
python3 stats.py -u farr/users-merged.txt  -b "2013-01-01 00:00:01" -e "2017-01-01 00:00:00" -p oldfarr_allnodes -d sgelogs
python3 stats.py -u farr/users-merged.txt  -b "2013-01-01 00:00:01" -e "2017-01-01 00:00:00" -p newfarr_allnodes
python3 stats.py -u farr/users-merged.txt -n farr/nodes.new -b "2013-01-01 00:00:01" -e "2017-01-01 00:00:00" -p newfarr_farrnodes