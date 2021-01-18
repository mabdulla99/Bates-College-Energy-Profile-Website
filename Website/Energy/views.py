from django.shortcuts import render
from .forms import ObservationForm, InputForm
from .models import Observation
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.core import serializers
from .plot import plotter


def index(request):
    form = InputForm

    def processed_data(name):

        data = serializers.serialize('python', Observation.objects.filter(building=name),
                                     fields=('Quantity', 'Time'))

        actual_data = [d['fields'] for d in data]  # returns a list of dict objects

        time_data = [item['Time'] for item in actual_data]
        energy_data = [item['Quantity'] for item in actual_data]

        return [time_data, energy_data]

    if request.method == 'POST':

        form = InputForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            building_list = data['building']  # comes out as a str

            #  cleaning building_list to obtain individual building names

            building_list = building_list.strip('[')
            building_list = building_list.strip(']')
            final_list = []
            for building in building_list.split(', '):
                final_list.append(building.strip("'"))

            #  returning dict with data for each requested building

            dataset = {}
            for building in final_list:
                dataset[building] = processed_data(building)

            plot = plotter(dataset)

            context_dict = {'form': form, 'plot': plot}

            return render(request, 'energy/index.html', context_dict)

        else:

            referrer = request.META['HTTP_REFERER']

            if referrer.endswith('energy/'):
                message = "You must make at least one selection!"

            context_dict = {'form': form, 'message': message}

            return render(request, 'energy/index.html', context_dict)
    else:

        context_dict = {'form': form}

        return render(request, 'energy/index.html', context_dict)


def about(request):
    context_dict = {}

    return render(request, 'energy/about.html', context_dict)


def user_login(request):
    next_tag = request.GET.get('next')  # to check what page the user came from.

    if next_tag is None:
        message = "Log in below."  # in the case where the user directly goes to the login page.
    else:
        message = "You must first login to view this page!"

    next = request.POST.get('next')  # to check what page the user must be sent to after logging in

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            if next == "":
                return HttpResponseRedirect(reverse('index'))

            else:
                print(next)
                return HttpResponseRedirect(next)

        else:

            message = "Invalid login details supplied. Try again!"
            context_dict = {'message': message}

            return render(request, 'Energy/login.html', context_dict)

    else:
        return render(request, 'Energy/login.html', {'next': next, 'message': message})


@login_required
def upload_data(request):
    form = ObservationForm

    if request.method == 'POST':

        form = ObservationForm(request.POST, request.FILES)

        if form.is_valid():

            files = request.FILES.getlist('file')

            for iter in range(len(files)):
                file_wrapper = files[iter]
                file = file_wrapper.file
                form.save(file)
                print("Saved all data in file number {}".format(iter + 1))

            return index(request)

        else:

            message = mark_safe("Invalid file format detected. Please try again! "
                                "Remember: <b> only .csv file extensions are allowed. <b/>")
            context_dict = {'form': form, 'message': message}

            return render(request, 'energy/upload.html', context_dict)
    else:

        message = mark_safe("To submit additional data, simply select the required files below and hit upload. "
                            "<b> NOTE: only .csv extensions will be accepted. <b/>")
        context_dict = {'form': form, 'message': message}

        return render(request, 'energy/upload.html', context_dict)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
