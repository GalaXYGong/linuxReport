#!/bin/bash
# dpkg -l | awk 'NR>5 {print $2 "," $3}' > ubuntuReport.csv
dpkg -l | awk 'BEGIN {print "["} NR>5 {printf "%s{\"package\":\"%s\",\"version\":\"%s\"}", (count++ ? "," : ""), $2, $3} END {print "\n]"}' > ubuntuReport.json