from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import Context, loader
from django.contrib.auth import authenticate, login
from django.template import Context, RequestContext, loader

from django.contrib import messages

from tools.models import Tool
from user.models import Owner
from shed.models import Shed

from user.admin import UserCreationForm
from user.forms import EditInfoForm, EditZipCodeForm

def index(request):
    if request.user.is_authenticated():
        # display user home page
        return render(request, "user/index.html")
        #return HttpResponse("Welcome, you are logged in")
        
    else:
        # display login/register page
        # uncomment render to test
        #template = loader.get_template('user/index.html')
        #context = RequestContext(request)
        
        return render(request, "user/login.html")
    
def home(request):
    return index(request)

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        
        # Auto-redirect to login after successful registration
        return redirect('/login/', new=True)
    else:
        messages.error(request, 'There is invalid information. Please double-check all inputs, including password.')
        return addRegisterForm(request)
        

def addRegisterForm(request):
    form = UserCreationForm(request.POST)
    context = Context({'title': 'Register', 'form': form})
    return render(request, 'user/registration.html', context)

def editInfo(request):
    if request.user.is_authenticated():
        owner = request.user
    form = EditInfoForm(request.POST, instance=owner)
    if form.is_valid():
        form.save()

    else:
        return editInfoForm(request)

    return redirect('/')

def editInfoForm(request):
    if request.user.is_authenticated():
        owner = request.user
        form = EditInfoForm(instance=owner)
        context = Context({'title': 'Edit Info', 'form': form})
        return render(request, 'user/editInfo.html', context)
    else:
        return HttpResponse("Please log in to edit your info")

def editZipCode(request):
    if request.user.is_authenticated():
        owner = request.user
        if request.method == 'POST':
            form = EditZipCodeForm(request.POST, instance=owner)
            if form.is_valid():
                borrowed_tools = Tool.objects.filter(borrower_id=owner.id)
                tools_on_loan = Tool.objects.filter(owner_id=owner.id).filter(availability=0)
                public_sheds = Shed.objects.filter(private=False)
                public_tools = []
                my_public_tools = []
                my_public_sheds = public_sheds.filter(owner_id=owner.id)

                for shed in public_sheds:
                    try:
                        public_tools.append(Tool.objects.filter(shed_id=shed.id))
                    except Tool.DoesNotExist:
                        pass

                for tool in public_tools:
                    try:
                        my_public_tools.append(Tool.objects.get(owner_id=owner.id))
                    except Tool.DoesNotExist:
                        pass

                if not borrowed_tools and not tools_on_loan and not my_public_tools and not my_public_sheds:
                    form.save()
                    messages.success(request, "Zip Code changed successfully")

                if borrowed_tools:
                    messages.error(request, "You are currently borrowing someone's tool, \
                        please return it before changing your zip code")

                if my_public_tools:
                    messages.error(request, "You currently have tools in a public shed, \
                        please move them to a private shed or remove them before changing your zip code")

                if tools_on_loan:
                    messages.error(request, "You currently have a tool on loan, \
                        please get it back before changing your zip code")

                if my_public_sheds:
                    messages.error(request, "You are currently the coordinator of a public shed,\
                        please remove this shed before changing your zip code")
                return redirect('/../editInfo')


            else:
                context= Context({'form':form})
                return render(request, 'user/editZipCode.html', context)

        else:
            form = EditZipCodeForm(instance=owner)
            context = Context({'form': form})
            return render(request, 'user/editZipCode.html', context)

def viewStatistics(request):
    if request.user.is_authenticated():
        try:
            sorted_tools = Tool.objects.order_by('usage_count').reverse()[:5]
            sorted_borrower = Owner.objects.order_by('borrow_counter').reverse()[:5]
            sorted_lender = Owner.objects.order_by('lend_counter').reverse()[:5]

            context = RequestContext(request, {
                'sorted_tools': sorted_tools,
                'sorted_borrower': sorted_borrower,
                'sorted_lender': sorted_lender,
                })

        except Tool.DoesNotExist:
            messages.error(request, 'There are no tools!')
            return redirect('/../tools/')

        return render(request, 'user/viewStatistics.html', context)

    else:
        return HttpResponseRedirect('/login')