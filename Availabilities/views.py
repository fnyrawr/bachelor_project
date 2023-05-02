from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Availability
from .forms import AvailabilityForm


class AvailabilityCreationView(CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availabilities/create_availability.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # delete entry if exists and create new
            availability = Availability.objects.filter(employee=request.POST['employee'],
                                                       weekday=request.POST['weekday'])
            if availability is not None:
                availability.delete()
            availability = form.save()
            messages.success(request, "Availability successfully created.")
            return redirect('availabilities')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


class OwnAvailabilityCreationView(CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'availabilities/add_own_availability.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # delete entry if exists and create new
            availability = Availability.objects.filter(employee=request.user,
                                                       weekday=request.POST['weekday'])
            if availability is not None:
                availability.delete()
            availability = form.save()
            messages.success(request, "Availability successfully created.")
            return redirect('own_availabilities')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def edit_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)

    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        data = form.data
        if 'is_available' in data:
            is_available = True
        else:
            is_available = False
        if data['start_time'] == '':
            start_time = None
        else:
            start_time = data['start_time']
        if data['end_time'] == '':
            end_time = None
        else:
            end_time = data['end_time']
        Availability.objects.filter(id=availability_id).update(
            employee=data['employee'],
            weekday=data['weekday'],
            is_available=is_available,
            start_time=start_time,
            end_time=end_time,
            tendency=data['tendency'],
            note=data['note']
        )
        messages.success(request, "Availability has been successfully updated.")
        return redirect('availabilities')
    # GET request
    else:
        employees = User.objects.all()
        form = AvailabilityForm()
        context = {
            'form': form,
            'selected_availability': selected_availability,
            'employees': employees
        }
        return render(request, 'availabilities/edit_availability.html', context)


def edit_own_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)

    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        data = form.data
        if 'is_available' in data:
            is_available = True
        else:
            is_available = False
        if data['start_time'] == '':
            start_time = None
        else:
            start_time = data['start_time']
        if data['end_time'] == '':
            end_time = None
        else:
            end_time = data['end_time']
        Availability.objects.filter(id=availability_id).update(
            employee=data['employee'],
            weekday=data['weekday'],
            is_available=is_available,
            start_time=start_time,
            end_time=end_time,
            tendency=data['tendency'],
            note=data['note']
        )
        messages.success(request, "Availability has been successfully updated.")
        return redirect('own_availabilities')
    # GET request
    else:
        form = AvailabilityForm()
        context = {
            'form': form,
            'selected_availability': selected_availability
        }
        return render(request, 'availabilities/edit_own_availability.html', context)


def delete_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)
    selected_availability.delete()
    messages.success(request, "Availability successfully deleted.")
    return redirect('availabilities')


def delete_own_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)
    selected_availability.delete()
    messages.success(request, "Availability successfully deleted.")
    return redirect('own_availabilities')


def own_availabilities(request):
    user = request.user
    all_entries = None
    all_entries = Availability.objects.filter(employee=user).order_by('weekday')

    context = {
        'all_entries': all_entries
    }
    return render(request, 'availabilities/own_availabilities.html', context)


def availability_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Availability.objects.all()

    context = {
        'all_entries': all_entries
    }
    return render(request, 'availabilities/availability_list.html', context)
