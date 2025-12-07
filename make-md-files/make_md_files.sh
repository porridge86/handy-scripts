#!/bin/bash

# create .md-file from the list in timeplan.txt
while read line; do
  touch "${line}.md"
done < timeplan.txt
