from django.db import models
from django.utils import timezone
from user.models import Owner
from tools.models import Tool
from shed.models import Shed

"""
Notification class used for display
Note that message is the optional message called for in requirements doc

The actual printout will be done in the template
"""
class Notification:

    def __init__(self,  not_type, receiver_id, sender_id, tool_id, shed_id, read, timestamp, \
        return_date, receiver_string, sender_string, tool_string, shed_string, message=""):
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.tool_id = tool_id
        self.shed_id = shed_id
        self.message = message
        self.not_type = not_type # Type of notification, see below
        self.timestamp = timestamp
        self.read = read
        
        self.receiver_string = receiver_string
        self.sender_string = sender_string
        self.tool_string = tool_string
        self.shed_string = shed_string

        self.return_date = return_date
        #if not_type == 0:
            #self.notif_msg = self.sender_string + ' borrowed your ' + self.tool_string + ' from shed ' + self.shed_string + '. '+ 'He/She will return it by ' + self.return_date


""" 
OwnerPublicToolBorrowed
type: 0
Sent to the owner of a tool when it is borrowed from pub shed 

OwnerPrivateToolRequested  
type: 1  
Sent to the owner of a tool when a private tool is requested
REQUIRES OWNER ACTION 
REQUIRES MESSAGE

OwnerPublicToolReturned
type: 2
Sent to the owner of a tool when a public tool is returned to a shed,
including when he confirms a private tool has returned

OwnerPrivateToolReturned
type: 3
Sent to the owner of a tool when a borrower asks 
him to confirm that a tool was returned
REQUIRES OWNER ACTION

BorrowerFailedToReturn
type: 4
Sent to the borrower of a tool when he claims a tool was
returned but the owner denies that it was returned

BorrowerPublicToolBorrowed
type: 5
Sent to the borrower of a tool when he borrows from a pub shed OR
when a private request is accepted

BorrowerPrivateToolRequested
type: 6        
Sent to the borrower of a tool when he requests a private tool 

BorrowerPrivateToolDenied
type: 7
Sent to the borrower of a tool when the owner denies his request
REQUIRES MESSAGE

OwnerToolNotReturned
type: 8
Sent to the owner of a tool when the tool is not returned past the
expected date.

BorrowerToolNotReturned
type: 9
Sent to the borrower of the tool when the tool is returned past the
expected date.

"""   

