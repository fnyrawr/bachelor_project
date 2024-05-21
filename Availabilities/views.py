from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Availability
from .forms import AvailabilityForm, SearchForm


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
        return HttpResponse(render(request, self.template_name, {'form': form}))


class OwnAvailabilityCreationView(CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'attendance/fragments/add_own_availability.html'

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
        return HttpResponse(render(request, 'attendance/fragments/edit_own_availability.html', context))


def delete_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)
    user = request.user
    if user.role == 'A':
        selected_availability.delete()
        messages.success(request, "Availability successfully deleted.")
    return redirect('availabilities')


def delete_own_availability(request, **kwargs):
    availability_id = kwargs['pk']
    selected_availability = Availability.objects.get(id=availability_id)
    user = request.user
    if selected_availability.employee == user:
        selected_availability.delete()
        messages.success(request, "Availability successfully deleted.")
    return redirect('own_availabilities')


def own_availabilities(request):
    user = request.user
    all_entries = Availability.objects.filter(employee=user).order_by('weekday')

    context = {
        'all_entries': all_entries
    }
    if all_entries.count() == 0:
        return HttpResponse('<h6><i class="material-icons accent-color-text left">info</i>No availabilities set</h6>')
    return HttpResponse(render(request, 'attendance/fragments/own_availabilities.html', context))


def availability_list(request):
    data = None
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_weekday = data['filter_weekday']
        filter_tendency = data['filter_tendency']
        keyword = data['keyword']
        q_weekday = Q()
        q_tendency = Q()
        q_keyword = Q()

        if int(filter_weekday) > 0:
            q_weekday = Q(weekday__exact=filter_weekday)
        if int(filter_tendency) > -1:
            q_tendency = Q(tendency__exact=filter_tendency)
        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | note)
        q = Q(q_weekday & q_tendency & q_keyword)
        entries = Availability.objects.filter(q)
    else:
        filter_weekday = datetime.today().weekday()+1
        searchForm = SearchForm()
        data = searchForm.data
        data['filter_weekday'] = filter_weekday
        q_weekday = Q(weekday__exact=filter_weekday)
        entries = Availability.objects.filter(q_weekday)

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data
    }
    return render(request, 'availabilities/availability_list.html', context)
