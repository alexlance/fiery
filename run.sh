#!/bin/bash

if [ "$1" == "-f" ]; then
  aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" > instances
  aws ec2 describe-security-groups > security
fi


cat <<EOD > index.html
<style>
table {
  border-spacing:0px;
}
tr:nth-child(even) {
  background-color:#eee;
}
th, td {
  padding:4px;
  text-align:left;
  white-space:nowrap;
}
</style>
<table>
<tr><th>Instance ID</th><th>Name</th><th colspan="100">Is open to...</th></tr>
$(python fiery.py)
</table>
EOD

#python fiery.py >> index.html
#echo "</table>" >> index.html
