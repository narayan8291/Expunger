# Expunger
Interactive python script for bulk slack deletes

## Use Case
Script can be used to bulk delete files from a Slack workspace. The script provides more control over the deletion process by allowing deletion,

1. Delete files belonging to a particular Slack channel.
2. Delete files belonging to a user. 
3. Delete files older than x days
4. Delete certain types of files. Options are listed here: https://api.slack.com/methods/files.list#file_types
5. Have a maximum cap on the number of files to be deleted. 

NOTE: All the above options can be used in tandem. 

## Script Execution

```python index.py```
