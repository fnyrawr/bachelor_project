from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Holiday
from .forms import HolidayForm


class HolidayCreationView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holidays/create_holiday.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            holiday = form.save()
            messages.success(request, "Holiday successfully created.")
            return redirect('holidays')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


class OwnHolidayCreationView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holidays/add_own_holiday.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            holiday = form.save()
            messages.success(request, "Holiday successfully created.")
            return redirect('own_holidays')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def edit_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    selected_holiday = Holiday.objects.get(id=holiday_id)

    if request.method == "POST":
        form = HolidayForm(request.POST)
        data = form.data
        Holiday.objects.filter(id=holiday_id).update(
            employee=data['employee'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data['status'],
            note=data['note']
        )
        messages.success(request, "Holiday has been successfully updated.")
        return redirect('holidays')
    # GET request
    else:
        employees = User.objects.all()
        form = HolidayForm()
        context = {
            'form': form,
            'selected_holiday': selected_holiday,
            'employees': employees
        }
        return render(request, 'holidays/edit_holiday.html', context)


def edit_own_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    selected_holiday = Holiday.objects.get(id=holiday_id)

    if request.method == "POST":
        form = HolidayForm(request.POST)
        data = form.data
        Holiday.objects.filter(id=holiday_id).update(
            status=data['status'],
            note=data['note']
        )
        messages.success(request, "Holiday has been successfully updated.")
        return redirect('own_holidays')
    # GET request
    else:
        form = HolidayForm()
        context = {
            'form': form,
            'selected_holiday': selected_holiday
        }
        return render(request, 'holidays/edit_own_holiday.html', context)


def delete_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    selected_holiday = Holiday.objects.get(id=holiday_id)
    selected_holiday.delete()
    messages.success(request, "Holiday successfully deleted.")
    return redirect('holidays')


def delete_own_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    selected_holiday = Holiday.objects.get(id=holiday_id)
    selected_holiday.delete()
    messages.success(request, "Holiday successfully deleted.")
    return redirect('own_holidays')


def own_holidays(request):
    user = request.user
    all_entries = None
    all_entries = Holiday.objects.filter(employee=user).order_by('start_date')

    context = {
        'all_entries': all_entries
    }
    return render(request, 'holidays/own_holidays.html', context)


def holiday_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Holiday.objects.all()

    context = {
        'all_entries': all_entries
    }
    return render(request, 'holidays/holiday_list.html', context)