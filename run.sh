#!/bin/bash
set -euo pipefail

#aws --output json ec2 describe-instances --filters "Name=instance-state-name,Values=running" > instances
#aws --output json ec2 describe-security-groups > security

#aws route53 list-hosted-zones
#aws route53 list-resource-record-sets --hosted-zone-id /hostedzone/Z37U77JFK8ZB1M


cat <<EOD > index.html

<script src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>

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
<table class="sortable">
<tr><th>Zone</th><th>Instance ID</th><th>IP</th><th>IP</th><th>Name</th><th colspan="100">Is open to...</th></tr>
$(python fiery.py)
</table>
EOD
