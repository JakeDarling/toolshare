"""
ToolShare Project
Team E
"""
from shed.models import Shed
from shed.forms import ShedForm, EditShedForm
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect


from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from tools.models import Tool
from user.models import Owner


def index(request):
    """Displays the index page (menu) of the shed model."""
    if request.user.is_authenticated():
        return render(request, 'shed/index.html')
    else:
        return HttpResponseRedirect('/login')
    
def addForm(request):
    """
    Renders the form to add a tool.
    """
    if request.user.is_authenticated():

        form = ShedForm()
        context = ({'title': 'Add Shed', 'form': form})
        return render(request, 'shed/addForm.html', context)
    else:
        return HttpResponseRedirect('/login')
    
def add(request):
    """
    This is the function that the addForm calls when a form
    is submitted. The new shed is added to the Shed database.
    Takes user back to the shed list.

    shed: new shed to be created from the information obtained from POST
    """
    if request.user.is_authenticated():
        form = ShedForm(request.POST)
        if form.is_valid():
            user_name= Owner.objects.get(pk=request.user.id).fname + ' ' + Owner.objects.get(pk=request.user.id).lname
            shed = Shed.objects.create(
                name=form.cleaned_data['name'],
                address_one=form.cleaned_data['address_one'],
                address_two=form.cleaned_data['address_two'],
                zipcode=form.cleaned_data['zipcode'],
                owner_id=request.user.id,
                owner_string=user_name,
                private=form.cleaned_data['private'],
            )
            shed_list = Shed.objects.filter(zipcode=request.user.zipcode)
            context = RequestContext(request, {
                'shed_list': shed_list
            })
            messages.success(request, 'The Shed has been successfully added.')
            return redirect('/../shed/viewSheds/')
        else:
            messages.error(request, 'There is invalid information. Please double-check all inputs.')
            return redirect('shed:addForm')
    else:
        return HttpResponseRedirect('/login')
    
def viewSheds(request):
    """
    Lists out all the sheds located in the shed's zipcode.
    Can click on the name to view it in detail.

    shed_list: entire Shed database
    """
    if request.user.is_authenticated():
        shed_list = Shed.objects.filter(zipcode=request.user.zipcode)
        context = RequestContext(request, {
            'shed_list': shed_list
        })
        return render(request, 'shed/viewSheds.html', context)
    else:
        return HttpResponseRedirect('/login')

def editShed(request, shed_id):
    """
    Edit a shed's information including name and location
    """
    if request.user.is_authenticated():
        shed = Shed.objects.get(pk=shed_id)
        if shed.owner_id == request.user.id:
            if request.method == 'POST':
                form = EditShedForm(request.POST, instance=shed)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Shed edited successfully")
                    tool_list = Tool.objects.filter(shed_id=shed_id)
                    context = RequestContext(request, {
                        'tool_list': tool_list,
                        'shed': shed,
                    })
                    return render(request, 'shed/detailShed.html', context)
            else:
                form = EditShedForm(instance=shed)
                context = Context({'form': form, 'shed': shed})
                return render(request, 'shed/editShed.html', context)
        else:
            messages.error(request, "You need to be the owner of a shed to edit it")
            return HttpResponseRedirect('/shed/detailShed/'+shed_id)
    else:
        return HttpResponseRedirect('/login')


def detailShed(request, shed_id):
    """
    Displays the tools located in the shed.

    tool_list: tools filtered by shed_id
    shed: the shed requested by shed_id
    """
    if request.user.is_authenticated():
        shed = Shed.objects.get(pk=shed_id)
        tool_list = Tool.objects.filter(shed_id=shed_id)
        context = RequestContext(request, {
            'tool_list': tool_list,
            'shed': shed,
        })
        return render(request, 'shed/detailShed.html', context)
    else:
        return HttpResponseRedirect('/login')

def removeShed(request, shed_id):
    """
    Removes the shed from the database. This is accessed by the remove link
    from the tool list. Redirects back to the shed list after removal.

    shed: shed obtained by shed_id requested
    """
    if request.user.is_authenticated():
        shed = Shed.objects.get(pk=shed_id)
        tool_list = Tool.objects.filter(shed_id=shed_id)
        if tool_list.exists():
            messages.error(request, 'There are still tools inside! The Shed must be empty before it can be removed.')
            return redirect('/../shed/viewSheds/')
        else:
            if request.user.id == shed.owner_id:
                shed.delete()
                shed_list = Shed.objects.filter(zipcode=request.user.zipcode)
                context = RequestContext(request, {
                    'shed_list': shed_list,
                })
                messages.success(request, 'The Shed has been removed.')
                return redirect('/../shed/viewSheds/')
            else:
                return HttpResponse('Only the owner can remove the shed!')
    else:
        return HttpResponseRedirect('/login')
