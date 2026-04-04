#!/bin/bash
# generate a report filename with the host_name, current date and time
report_filename="$(hostname)_$(date +%Y%m%d%H%M%S)"
dpkg -l | awk 'NR>5 {print $2 "," $3}' > ${report_filename}.csv
dpkg -l | awk 'BEGIN {print "["} NR>5 {printf "%s{\"package\":\"%s\",\"version\":\"%s\"}", (count++ ? "," : ""), $2, $3} END {print "\n]"}' > ${report_filename}.json