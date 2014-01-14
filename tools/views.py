"""
ToolShare Project
Team E
"""
import pdb

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from tools.models import Tool
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from datetime import date, timedelta
from django.contrib import messages
from django.utils import timezone

from django.template import Context, RequestContext, loader

from django.shortcuts import render, render_to_response, get_object_or_404
from tools.forms import ToolForm, BorrowForm, DenyForm
from shed.models import Shed
from user.models import Owner
from notifications.models import Notification
from notifications.views import *
"""
def dbCheck(request):
    borrowed_tools = Tool.objects.filter(borrower_id=request.user.id)
    owned_tools = Tool.objects.filter(owner_id=request.user.id)
    if borrowed_tools:
        for tool in borrowed_tools:
            if tool.return_date < date.today():
                #Send notification
                current_time = timezone.now()

                n1 = Notification(8, tool.borrower_id, request.user.id, \
                    tool.id, tool.shed_id, 1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), \
                    tool.return_date, tool.borrower_string, request.user.fname + ' ' + request.user.lname, \
                    tool.name, tool.shed_string)
                n2 = Notification(9, request.user.id, request.user.id, \
                    tool.id, tool.shed_id, 1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), \
                    tool.return_date, request.user.fname + ' ' + request.user.lname, \
                    request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
                log_notification(n1)
                log_notification(n2)
                setattr(tool, 'availability', 2)
    if owned_tools:
        for tool in owned_tools:
            if tool.return_date < date.today():
                #Send notification
                current_time = timezone.now()

                n1 = Notification(8, tool.borrower_id, request.user.id, \
                    tool.id, tool.shed_id, 1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), \
                    tool.return_date, tool.borrower_string, request.user.fname + ' ' + request.user.lname, \
                    tool.name, tool.shed_string)
                n2 = Notification(9, request.user.id, request.user.id, \
                    tool.id, tool.shed_id, 1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), \
                    tool.return_date, request.user.fname + ' ' + request.user.lname, \
                    request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
                log_notification(n1)
                log_notification(n2)
                setattr(tool, 'availability', 2)
"""
def index(request):
    """Displays the index page (menu) of the tools model."""
    #dbCheck(request)
    if request.user.is_authenticated():
        unread_messages = count_unread(request.user.id)
        if unread_messages != None:
            context = RequestContext(request, {
                'unread_messages': unread_messages,
                })
            return render(request, 'tools/index.html', context)
        else:
            return render(request, 'tools/index.html')
    else:
        #If user is not logged in, will redirect to login page.
        return HttpResponseRedirect('/login')

def viewTools(request):
    """
    Lists out all the tools located in the user's zipcode.
    Can click on the name to view it in detail.

    tool_list: entire Tool database
    """
    tool_list = Tool.objects.all()
    if request.user.is_authenticated(): #If user is logged in
        context = RequestContext(request, {
            'tool_list': tool_list,
        })

        return render(request, 'tools/viewTools.html', context)
    else:
        return HttpResponseRedirect('/login')

def viewMyTools(request):
    """
    Lists out all the tools that the user owns.

    tool_list: Tool database filtered by user's ID
    """
    tool_list = Tool.objects.filter(owner_id=request.user.id)
    if request.user.is_authenticated(): #If user is logged in
        context = RequestContext(request, {
            'tool_list': tool_list,
        })

        return render(request, 'tools/viewTools.html', context)
    else:
        return HttpResponseRedirect('/login')

def viewBorrowedTools(request):
    """
    Lists out all the tools that the user is currently borrowing.

    tool_list: Tool database filtered by borrower's ID.
    """
    tool_list = Tool.objects.filter(borrower_id=request.user.id)
    if request.user.is_authenticated():
        context = RequestContext(request, {
            'tool_list': tool_list,
        })
        return render(request, 'tools/viewTools.html', context)
    else:
        return HttpResponseRedirect('/login')

def detail(request, tool_id):
    """
    Displays the tool information in detail, such as Shed Location
    and Description. If the tool is public, render the detail.html page
    If the tool is private, render the detailprivate.html page.
    The two pages are identical except that the form submission redirects
    to two different functions.

    tool: tool row obtained by tool_id requested
    shed_name: Shed's name obtained by tool's shed_id
    dates_list: list of dates determined by the return date limit
    """
    if request.user.is_authenticated(): #If user is logged in
        tool = Tool.objects.get(pk=tool_id)
        if Shed.objects.get(pk=tool.shed_id).private == False:
            shed_name = Shed.objects.get(pk=tool.shed_id).name
            user_current_date = request.user.id
            dates_list = []
            days_number = tool.return_date_limit
            for day_count in range(tool.return_date_limit):
                new_day_count = day_count
                today_and_next = date.today()+timedelta(days=new_day_count)
                dates_list.append(today_and_next.strftime("%m/%d/%Y"))
                    
            context = RequestContext(request, {
                'tool': tool,
                'shed_name': shed_name,
                'dates_list': dates_list,
            })
            return render(request, 'tools/detail.html', context)
        if Shed.objects.get(pk=tool.shed_id).private == True:
            shed_name = Shed.objects.get(pk=tool.shed_id).name
            user_current_date = request.user.id
            dates_list = []
            days_number = tool.return_date_limit
            for day_count in range(tool.return_date_limit):
                new_day_count = day_count
                today_and_next = date.today()+timedelta(days=new_day_count)
                dates_list.append(today_and_next.strftime("%m/%d/%Y"))
                    
            context = RequestContext(request, {
                'tool': tool,
                'shed_name': shed_name,
                'dates_list': dates_list,
            })
            return render(request, 'tools/detailprivate.html', context)
    else:
        return HttpResponseRedirect('/login')


def addToolForm(request, id=None):
    """
    Renders the form to add a tool.

    NOTE: The edit portion of this function IS NOT USED
    """
    if request.user.is_authenticated():
        first_shed_list = Shed.objects.filter(zipcode=request.user.zipcode)
        shed_list = []
        for shed in first_shed_list:
            if shed.owner_id == request.user.id or shed.private == 0:
                shed_list.append(shed)
            else:
                pass
        if len(shed_list) > 0:
            form = ToolForm()
            context = ({'title': 'Add Tool',
                        'form': form,
                        'shed_list': shed_list,
            })
            return render(request, 'tools/addToolForm.html', context)
        else:
            messages.error(request, 'There are no Sheds in this Zipcode to store the Tool in. Please create a Shed first.')
            return redirect('/../tools/')
    else:
        return HttpResponseRedirect('/login')

def addTool(request):
    """
    This is the function that the addToolForm calls when a form
    is submitted. The new tool is added to the Tool database.
    Takes user back to the tool list.

    tool: new tool to be created from the information obtained from POST
    """
    if request.user.is_authenticated(): #If user is logged in
        form = ToolForm(request.POST, request.FILES)
        tool_list = Tool.objects.all()
        if form.is_valid():
            tool = Tool.objects.create(
                name=form.cleaned_data['name'],
                owner_id=request.user.id,
                owner_string=Owner.objects.get(pk=request.user.id).fname + ' ' + Owner.objects.get(pk=request.user.id).lname,
                borrower_id=0,
                borrower_string='None',
                availability=1,
                shed_id = form.cleaned_data['shed_id'],
                shed_string = Shed.objects.get(pk=form.cleaned_data['shed_id']).name,
                zipcode = Shed.objects.get(pk=form.cleaned_data['shed_id']).zipcode,
                description=form.cleaned_data['description'],
                creation_date = date.today(),
                return_date_limit = form.cleaned_data['return_date_limit'],
                return_date = '2001-01-01',
                usage_count = 0,
                image = form.cleaned_data['image'],
            )
            #return render(request, 'tools/addTool.html', context)
            context = RequestContext(request, {
                'tool_list': tool_list,
            })
            messages.success(request, 'The Tool has been added.')
            return render(request, 'tools/viewTools.html', context)

        else:
            messages.error(request, 'There is invalid information. Please double-check all inputs.')
            shed_list = Shed.objects.filter(zipcode=request.user.zipcode)
            form = ToolForm()
            context = ({'title': 'Add Tool',
                        'form': form,
                        'shed_list': shed_list,
            })
            return render(request, 'tools/addToolForm.html', context)
    else:
        #If not logged in, redirect to login page
        return HttpResponseRedirect('/login')


def editToolForm(request, tool_id):
    """
    Renders the edit tool form. Existing information will be inputted
    to the corresponding box.

    tool: obtained by tool_id requested
    shed_list: shed database
    form: ToolForm imported from forms.py
    """
    if request.user.is_authenticated():
        if request.user.id == Tool.objects.get(pk=tool_id).owner_id:
            tool = Tool.objects.get(pk=tool_id)
            shed_list = Shed.objects.all()
            form = ToolForm(instance=tool)
            context = Context({'title': 'Edit Tool', 'form': form, 'tool': tool, 'shed_list': shed_list })
            return render(request, 'tools/editTool.html', context)
        else:
            messages.error(request, 'You can only edit tools that you own.')
            return redirect('/../tools/viewTools/')
    else:
        #Placeholder for situation when user is not logged in.
        return HttpResponseRedirect('/login')

def editTool(request, tool_id):
    """
    Edits the tool's information obtained by the POST from editToolForm.

    form: form obtained by tool_id
    """
    if request.user.is_authenticated():
        if request.user.id == Tool.objects.get(pk=tool_id).owner_id:
            tool = Tool.objects.get(pk=tool_id)
            form = ToolForm(request.POST, instance=Tool.objects.get(pk=tool_id))
            if tool.availability == 1:
                if form.is_valid():
                    form.save()
                    tool = Tool.objects.get(pk=tool_id)
                    setattr(tool, 'shed_string', Shed.objects.get(pk=tool.shed_id).name) #Sets the string name of the tool's shed
                    setattr(tool, 'image', form.cleaned_data['image'])
                    tool.save()
                    messages.success(request, 'The tool has been edited.')
                    return redirect('/../tools/viewTools')
                else:
                    messages.error(request, 'The information you have entered is invalid.')
                    return redirect('tools:editToolForm', tool_id)
            else:
                messages.error(request, 'Cannot edit tool. Tool is either in request or is unavailable.')
                return redirect('tools:editToolForm', tool_id)
        else:
            messages.error(request, 'You can only edit tools that you own.')
            return redirect('/../tools/viewTools/') #If the tool does not belong to the user. PLACEHOLDER
    else:
        return HttpResponseRedirect('/login') #If the user is not logged in. PLACEHOLDER

    
def remove(request, tool_id):
    """
    Removes the tool from the database. This is accessed by the remove link
    from the tool list. Redirects back to the tool list after removal.

    tool: tool obtained by tool_id
    """
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        if request.user.id == tool.owner_id:
            if tool.availability == 1:
                tool.delete()
                messages.success(request, 'The tool has been successfully removed.')
                return redirect('/../tools/viewTools/')
            else:
                messages.error(request, 'The tool selected is either unavailable or currently being requested.')
                return redirect('/../tools/viewTools/')
        else:
            messages.error(request, 'You can only remove tools that you own.')
            return redirect('/../tools/viewTools/')
    else:
        #If user is not logged in, redirect to login page
        return HttpResponseRedirect('/login')


def borrowRequest(request, tool_id):
    """
    Private tool only. Sends a notification to both tool owner and requester.
    Tool owner will receive a notification that has an Accept/Deny message.
    Requester receives a reminder message.
    """
    if request.user.is_authenticated():
        form = BorrowForm(request.POST)
        if form.is_valid():
            return_date = form.cleaned_data['return_date']
            tool = Tool.objects.get(pk=tool_id)
            tool.availability = 2
            tool.save()
            current_time = timezone.now()
            n1 = Notification(6, request.user.id, request.user.id, \
                tool_id, tool.shed_id, 1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), \
                return_date, request.user.fname + ' ' + request.user.lname, \
                request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
            log_notification(n1)
            n2 = Notification(1, tool.owner_id, request.user.id, tool_id, tool.shed_id, \
                1, current_time.strftime("%Y-%m-%d;%H-%M-%S"), return_date, \
                tool.owner_string, request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string, \
                form.cleaned_data['msg'])
            log_notification(n2)
            messages.success(request, 'The tool has been requested.')
            return redirect('/../tools/viewTools/')
        else:
            messages.error(request , 'There is invalid information.')
            return redirect('/../tools/viewTools/')
        
    else:
        return HttpResponseRedirect('/login')

def returnToolConfirmation(request, tool_id, timestamp):
    """
    Private tool only. Sends a notification to
    the tool owner Function executes when the private tool is confirmed
    to be returned. The tool will return to default, available state.
    """
    #Only for private tools
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        mark_read(request.user.id, timestamp)
        current_time = timezone.now()
        n1 = Notification(3, tool.owner_id, request.user.id, tool_id, \
            tool.shed_id, 1,current_time.strftime("%Y-%m-%d;%H-%M-%S"), '2001-01-01', \
            tool.owner_string, request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
        log_notification(n1)
        tool = Tool.objects.get(pk=tool_id)
        setattr(tool, 'availability', 1)
        setattr(tool, 'return_date', '2001-01-01')
        setattr(tool, 'borrower_id', 0)
        setattr(tool, 'borrower_string', 'None')
        tool.save()
        messages.success(request, 'The tool has been returned.')
        return redirect('/../notifications/view/')
    else:
        return HttpResponse("Please login")

def denyReturnToolConfirmation(request, tool_id, timestamp):
    """
    Private tool only. The information and state of the tool in question
    will remain the same. Sends a notification to the tool borrower that
    the tool has not been returned. The denier must include a reason/message.
    """
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        current_time = timezone.now()
        n1 = Notification(4, tool.borrower_id, request.user.id, tool_id, tool.shed_id, 1, \
            current_time.strftime("%Y-%m-%d;%H-%M-%S;%Z"), tool.return_date, tool.borrower_string, \
            request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
        messages.success(request, 'The tool has been confirmed to not have been returned. Please settle the conflict and then set it to be available again.')
        return redirect('/../notifications/view/')
    else:
        return HttpResponseRedirect('/login')

def denyRequestForm(request, tool_id, borrower_id, timestamp):
    """
    Renders a textbox so the tool owner can include message or reason
    as to why the tool is denied to the requester.
    """
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        form = DenyForm()
        context = RequestContext(request, {
            'tool': tool,
            'borrower_id': borrower_id,
            'timestamp': timestamp
            })
        return render(request, 'tools/denyForm.html', context)


def denyRequest(request, tool_id, borrower_id, timestamp):
    """
    Sends a notification to the requester that the request has been
    denied. The notification includes a reason why.
    """
    if request.user.is_authenticated():
        form = DenyForm(request.POST)
        tool = Tool.objects.get(pk=tool_id)
        if form.is_valid():
            current_time = timezone.now()
            n1 = Notification(7, borrower_id, tool.owner_id, tool_id, tool.shed_id, 1, \
                current_time.strftime("%Y-%m-%d;%H-%M-%S"), '2001-01-01', tool.borrower_string, 
                tool.owner_string, tool.name, tool.shed_string, form.cleaned_data['reason'])
            log_notification(n1)
            mark_read(request.user.id, timestamp)

            messages.success(request, 'The request has been denied.')
            return redirect('/../notifications/view')
        else:
            messages.error(request, 'The denial is invalid. It cannot be empty.')
            return redirect('/../notifications/view')
    else:
        return HttpResponseRedirect('/login')

def borrowTool(request, tool_id):
    """
    Public Tool only. Borrows a tool, changes the information of the
    tool. A notification is sent to the requester and the tool's shed's
    owner.
    """
    if request.user.is_authenticated():
        #Public Tool borrowing
        form = BorrowForm(request.POST)
        tool = Tool.objects.get(pk=tool_id)
        
        borrower = Owner.objects.get(pk=request.user.id)
        tool_owner = Owner.objects.get(pk=tool.owner_id)

        new_borrow_count = borrower.borrow_counter + 1
        new_lend_count = tool_owner.lend_counter + 1

        shed = Shed.objects.get(pk=tool.shed_id)

        new_usage_count = tool.usage_count + 1

        if tool.availability == 1:
            if form.is_valid():
                tool = Tool.objects.get(pk=tool_id)
                #Can get rid of boolean column, as 01-01-2001 will indicate availability
                setattr(tool, 'availability', 0)
                setattr(tool, 'return_date', form.cleaned_data['return_date'])
                setattr(tool, 'borrower_id', request.user.id)
                setattr(tool, 'borrower_string', Owner.objects.get(pk=request.user.id).fname + ' ' + Owner.objects.get(pk=request.user.id).lname)
                setattr(tool, 'usage_count', new_usage_count)
                current_time = timezone.now()

                
                setattr(tool_owner, 'lend_counter', new_lend_count)
                n1 = Notification(5, request.user.id, request.user.id, tool.id, tool.shed_id, 1, \
                    current_time.strftime("%Y-%m-%d;%H-%M-%S;%Z"), tool.return_date, \
                    request.user.fname + ' ' + request.user.lname, request.user.fname + ' ' + request.user.lname, \
                    tool.name, tool.shed_string)

                setattr(borrower, 'borrow_counter', new_borrow_count)


                log_notification(n1)
                n2 = Notification(0, shed.owner_id, request.user.id, tool.id, tool.shed_id, 1, \
                    current_time.strftime("%Y-%m-%d;%H-%M-%S;%Z"), tool.return_date, \
                    shed.owner_string, request.user.fname + ' ' + request.user.lname, tool.name,
                    tool.shed_string)
                log_notification(n2)

                tool_owner.save()
                borrower.save()
                tool.save()
                messages.success(request, 'The tool has been borrowed.')
                return redirect('/../tools/viewTools/')
            else:
                messages.error(request, 'The information you have entered is not valid.')
                return redirect('/../tools/viewTools/')
        else:
            messages.error(request, 'The tool has already been borrowed.')
            return redirect('/../tools/viewTools/')
    else:
        return HttpResponseRedirect('/login')

def borrowPrivateTool(request, tool_id, borrower_id, return_date, timestamp):
    """
    Sets the tool to borrowed. Sends a notification to both tool requester and tool owner.
    """
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        usage_count = tool.usage_count
        new_usage_count = usage_count + 1
        if Shed.objects.get(pk=tool.shed_id).private == True:
            if tool.availability == 1 or tool.availability == 2:
                setattr(tool, 'availability', 0)
                setattr(tool, 'return_date', return_date)
                setattr(tool, 'borrower_id', borrower_id)
                setattr(tool, 'borrower_string', Owner.objects.get(pk=borrower_id).fname + ' ' + Owner.objects.get(pk=borrower_id).lname)
                setattr(tool, 'usage_count', new_usage_count)
                mark_read(request.user.id, timestamp)
                current_time = timezone.now()
                n1 = Notification(5, borrower_id, request.user.id, tool.id, tool.shed_id, 1, \
                    current_time.strftime("%Y-%m-%d;%H-%M-%S"), return_date, tool.borrower_string,
                    request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
                log_notification(n1)
                n2 = Notification(0, tool.owner_id, borrower_id, tool.id, tool.shed_id, 1, \
                    current_time.strftime("%Y-%m-%d;%H-%M-%S"), return_date, tool.owner_id,
                    tool.borrower_string, tool.name, tool.shed_string)
                log_notification(n2)
                tool.save()
                messages.success(request, 'The tool has been lent.')
                return redirect('/../notifications/view/')
            else:
                messages.error(request, 'The tool is not available.')
                return redirect('/../notifications/view/')
        else:
            messages.error(request, 'The tool is not private.')
            return redirect('/../notifications/view/')
    else:
        return HttpResponseRedirect('/login')
                            
def returnTool(request, tool_id):
    """
    Sets the public tool to default values.
    """
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        current_time = timezone.now()
        shed = Shed.objects.get(pk=tool.shed_id)
        if Shed.objects.get(pk=tool.shed_id).private == False:
            if request.user.id == tool.borrower_id:
                if tool.return_date != '01/01/2001':
                    setattr(tool, 'availability', 1)
                    setattr(tool, 'return_date', '2001-01-01')
                    setattr(tool, 'borrower_id', 0)
                    setattr(tool, 'borrower_string', 'None')
                    """
                    n1 = Notification(8, request.user.id, request.user.id, tool.id, tool.shed_id, 1, \
                        current_time.strftime("%Y-%m-%d;%H-%M-%S"), '2001/01/01', request.user.fname +
                        ' ' + request.user.lname, request.user.fname + ' ' + request.user.lname, tool.name,
                        tool.shed_string)
                    log_notification(n1)
                    """
                    n2 = Notification(2, shed.owner_id, request.user.id, tool.id, tool.shed_id, 1, \
                        current_time.strftime("%Y-%m-%d;%H-%M-%S;%Z"),'2001/01/01', shed.owner_string,
                        request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string)
                    log_notification(n2)
                    tool.save()
                    messages.success(request, 'The tool has been returned.')
                    return redirect('/../tools/')
                else:
                    messages.error(request, 'Tool is already available.')
                    return redirect('/../tools/viewTools/')
            else:
                messages.error(request, 'You are currently not the borrower of the tool.')
                return redirect('/../tools/viewTools/')
        elif Shed.objects.get(pk=tool.shed_id).private == True:
            if request.user.id == tool.borrower_id:
                if tool.return_date != '01/01/2001':
                    n2 = Notification(3, tool.owner_id, request.user.id, tool.id, tool.shed_id, 1, \
                        current_time.strftime("%Y-%m-%d;%H-%M-%S"), '2001/01/01', tool.owner_string, \
                        request.user.fname + ' ' + request.user.lname, tool.name, tool.shed_string )
                    log_notification(n2)
                    messages.success(request, 'The return confirmation has been sent to the owner of the tool. The tool will be returned when the owner confirms it.')
                    return redirect('/../tools/viewTools/')
                else:
                    messages.error(request, 'Tool is already available.')
                    return redirect('/../tools/viewTools/')
            else:
                messages.error(request, 'You are currently not the borrower of the tool.')
                return redirect('/../tools/viewTools/')
    else:
        return HttpResponseRedirect('/login')


def setAvailable(request, tool_id):
    if request.user.is_authenticated():
        tool = Tool.objects.get(pk=tool_id)
        if tool.availability != 1:
            setattr(tool, 'availability', 1)
            setattr(tool, 'return_date', '2001-01-01')
            setattr(tool, 'borrower_id', 0)
            setattr(tool, 'borrower_string', 'None')
            tool.save()
            messages.success(request, 'The tool is now available.')
            return redirect('/../tools/')
        else:
            messages.error(request, 'The tool is already available.')
            return redirect('/../notifications/view')
    else:
        return HttpResponseRedirect('/login')