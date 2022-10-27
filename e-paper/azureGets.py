import requests
import sys
import time
from datetime import *
import logging

def getVmStatus ():
	on = 0;
	### Get Bearer token ###
	url = 'https://login.microsoftonline.com/<Your tenant ID>/oauth2/token'
	body = {
		'grant_type'     : 'client_credentials',
		'tenantId'       : '<Your Tenant ID>',
		'client_id'      : '<Your Client ID>',
		'client_secret'  : '<Your Client Secret>',
		'resource'       : 'https://management.azure.com/',
		'subscriptionId' : '<Your subscription ID>'
	}
	BearerReq = requests.post(url, body)
	BearerReqContentDict = BearerReq.json()
	BearerToken = 'Bearer ' + BearerReqContentDict.get('access_token')
	### Get VM Status ###
	url = 'https://management.azure.com/subscriptions/<Your subsription ID>/resourceGroups/<Your resource group>/providers/Microsoft.Compute/virtualMachines/<Your VM name>/instanceView?api-version=2022-08-01'
	header = {'Authorization': BearerToken}
	VmStatusReq = requests.get(url, headers = header, timeout=10)
	logging.debug('getVMStatus HTTP response status code: ' + str(VmStatusReq.status_code))
	# Possible reponses: "VM running","VM deallocated"
	return VmStatusReq.json().get('statuses')[1]['displayStatus'];

def getBudget ():
	on = 0;
	### Get Bearer token ###
	url = 'https://login.microsoftonline.com/<Your tenant ID>/oauth2/token'
	body = {
		'grant_type'     : 'client_credentials',
		'tenantId'       : '<Your Tenant ID>',
		'client_id'      : '<Your Client ID>',
		'client_secret'  : '<Your Client Secret>',
		'resource'       : 'https://management.azure.com/',
		'subscriptionId' : '<Your subscription ID>'
	}
	BearerReq = requests.post(url, body)
	BearerReqContentDict = BearerReq.json()
	BearerToken = 'Bearer ' + BearerReqContentDict.get('access_token')
	### Get VM Status ###
	url = 'https://management.azure.com/subscriptions/<Your subsription ID>/providers/Microsoft.Consumption/budgets/totalcost?api-version=2021-10-01'
	header = {'Authorization': BearerToken}
	budgetReq = requests.get(url, headers = header, timeout=10)
	logging.debug('getBudget HTTP response status code: ' + str(budgetReq.status_code))
	return budgetReq.json().get("properties").get("currentSpend").get("amount");

def getCalendarEvents ():
        ### Get Bearer token ###
        url = 'https://login.microsoftonline.com/<Your tenant ID>/oauth2/token'
        body = {
                'grant_type'     : 'client_credentials',
                'tenantId'       : '<Your Tenant ID>',
                'client_id'      : '<Your Client ID>',
                'client_secret'  : '<Your Client Secret>',
                'resource'       : 'https://graph.microsoft.com',
                'scope' : 'https://graph.microsoft.com'
        }
        BearerReq = requests.post(url, body)
        BearerReqContentDict = BearerReq.json()
        BearerToken = 'Bearer ' + BearerReqContentDict.get('access_token')
        ### Get Calendar events ###
        url = 'https://graph.microsoft.com/v1.0/users/<Your user object ID>/events?$orderby=start/dateTime asc &filter='
        timeFilteringGE = 'start/dateTime ge \'' + str(datetime.strptime(str(datetime.today().date()),'%Y-%m-%d') + timedelta(hours=4)) + '\''
        timeFilteringLE = 'and start/dateTime le \'' + str( datetime.strptime(str(datetime.today().date()),'%Y-%m-%d') + timedelta(hours=4) + timedelta(days=1)) + '\''
        header = {'Authorization': BearerToken}
        calendarEventsReq = requests.get(url + timeFilteringGE + timeFilteringLE, headers = header, timeout=10)
        events = []
        for event in calendarEventsReq.json().get('value'):
                subject = event.get('subject')
                events.append(str((datetime.strptime(event.get('start').get('dateTime'),'%Y-%m-%dT%H:%M:%S.%f0') - timedelta(hours=4)).strftime('%m/%d %H:%M')) + ' - ' + subject)
        logging.debug('getCalendarEvents HTTP response status code: ' + str(calendarEventsReq.status_code))
        return events