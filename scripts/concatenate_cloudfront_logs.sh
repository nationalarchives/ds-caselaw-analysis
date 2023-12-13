#!/bin/bash

# Concatenate all the downloaded cloudfront files, leaving out the field headers
zcat $1 | grep -v ^\# > tmp/logs_unsorted_no_comments.log
# Sort them by timestamp
sort tmp/logs_unsorted_no_comments.log > tmp/logs_sorted_no_comments.log
# Reinsert the field headers at the top, tab separated.
first_file=`ls $1 | head -n 1`
zcat $first_file | grep Fields | sed s/^\#Fields:\ //g | sed -E s/\ /\    /g > $2
cat tmp/logs/sorted_no_comments.log >> $2
rm tmp/logs_unsorted_no_comments.log
rm tmp/logs_sorted_no_comments.log