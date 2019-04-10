import sys, time, requests, json
import config as cfgValues

def constructSlackURL(userArgsDict):
	try:
		returnURL = ""
		constructURL = ""
		for key,value in userArgsDict.iteritems():
			if value != "":
				constructURL += cfgValues.argumentDict[key] + '=' + value + '&'
		returnURL += cfgValues.baseURL + "?" + constructURL
		fileList = getFileIDs(str(returnURL[:len(returnURL)-1])) # removing the last &
		deleteCount = 0
		print "*** Deleting files ***"
		for fileID in fileList:
			if deleteFile(fileID, userArgsDict['slackToken']) == 1:
				deleteCount += 1
		print "Total number of files deleted: " + str(deleteCount)
	except Exception as e:
		print "Error in constructing the Slack URL: " + str(e)

def convertUnixTime(days):
    return int(time.time()) - int(days) * 24 * 60 * 60

def getFileIDs(slackUrl):
	try:
		fileIDList = []
		print "*** Getting file list from Slack ***"
		response = requests.get(slackUrl)
		fileJsonData = json.loads(response.text)['files']
		for individualFile in fileJsonData:
			fileIDList.append(individualFile['id'])
		userConsent = raw_input("File list has been fetched from Slack. There is a total of " + str(len(fileIDList)) + " files marked for deletion. Go ahead? Enter yes or no: ")
		if userConsent.lower() != "yes":
			exit("File deletion process has been stopped") 
		return fileIDList
	except Exception as e:
		print "Error in get file list from Slack: " + str(e)

def deleteFile(fileId,token):
    try:
    	url = cfgValues.deleteURL + "?token=" + str(token) + "&file=" + str(fileId)
    	response = requests.get(url)
    	responseJSON = json.loads(response.text)
    	if responseJSON['ok'] == True:
    		print "Deleted file: " + str(fileId)
    		return 1
    	else:
    		print "Failed to delete file: " + str(fileId) + ". Reason is: " + str(responseJSON['error']) + ". Check https://api.slack.com/methods/files.delete for more details on the error message."
    		return 0
    except Exception as e:
    	print "Error in deleting file: " + str(e)
    	return 0

if __name__ == "__main__":
	# Get values for constructing the URL for files.list => https://api.slack.com/methods/files.list
	# Construct Local Dict for passing user values
	userArgsDict = {}
	userArgsDict['slackToken'] = raw_input('Enter Slack Token (Required): ')
	'''slackToken is a required field'''
	if userArgsDict['slackToken'] == "":
		exit("Error => Slack token cannot be empty")
	userArgsDict['channelID'] = raw_input('Enter Channel ID (Optional): ')
	userArgsDict['fileCount'] = raw_input('Max number of files to be deleted at once (Optional). Default is 100: ')
	userArgsDict['days'] = raw_input('Delete files older that x days (Optional): ')
	# Convert to unix timestamp if not empty
	if userArgsDict['days'] != "":
		userArgsDict['days'] = str(convertUnixTime(userArgsDict['days']))
	userArgsDict['fileTypes'] = raw_input('File Types. See https://api.slack.com/methods/files.list#file_types for options (Optional): ')
	userArgsDict['userId'] = raw_input('Filter based on user id (Optional): ')
	constructSlackURL(userArgsDict)