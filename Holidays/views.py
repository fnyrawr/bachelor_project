import base64
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Shifts.models import Shift, ShiftQualifications
from Users.models import User
from utils.create_calendar import draw_calendar
from .models import Holiday
from .forms import HolidayForm, SearchForm


class HolidayCreationView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holidays/fragments/create_holiday.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            holiday = form.save()
            messages.success(request, "Holiday successfully created.")

            # unassign employee from conflicting shifts
            selected_holiday = holiday
            if selected_holiday.status == 3:
                q_employee = Q(employee=selected_holiday.employee)
                q_date_start = Q(start__gte=selected_holiday.start_date)
                q_date_end = Q(start__lte=selected_holiday.end_date)
                emp_name = selected_holiday.employee.first_name + ' ' + selected_holiday.employee.last_name
                Shift.objects.filter(Q(q_employee & q_date_start & q_date_end)).update(
                    employee_id=None,
                    highlight=True,
                    note=emp_name + ' on holiday'
                )
                messages.info(request, "Unassigned employee from conflicting shifts.")

            return redirect('holidays')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


class OwnHolidayCreationView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'attendance/fragments/add_own_holiday.html'

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

    # filter conflicting shifts
    q_employee = Q(employee=selected_holiday.employee)
    q_date_start = Q(start__gte=selected_holiday.start_date)
    q_date_end = Q(start__lte=selected_holiday.end_date)
    conflicting_shifts = Shift.objects.filter(Q(q_employee & q_date_start & q_date_end))
    for shift in conflicting_shifts:
        qualifications = ShiftQualifications.objects.filter(shift_id=shift.id).order_by(
            'qualification__name')
        shift.qualifications = qualifications

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

        # unassign employee from conflicting shifts
        selected_holiday = Holiday.objects.get(id=holiday_id)
        if selected_holiday.status == 3:
            q_employee = Q(employee=selected_holiday.employee)
            q_date_start = Q(start__gte=selected_holiday.start_date)
            q_date_end = Q(start__lte=selected_holiday.end_date)
            emp_name = selected_holiday.employee.first_name + ' ' + selected_holiday.employee.last_name
            Shift.objects.filter(Q(q_employee & q_date_start & q_date_end)).update(
                employee_id=None,
                highlight=True,
                note=emp_name + ' on holiday'
            )
            messages.info(request, "Unassigned employee from conflicting shifts.")

        messages.success(request, "Holiday has been successfully updated.")
        return redirect('holidays')
    # GET request
    else:
        employees = User.objects.all()
        form = HolidayForm()
        context = {
            'form': form,
            'selected_holiday': selected_holiday,
            'employees': employees,
            'conflicting_shifts': conflicting_shifts
        }
        return render(request, 'holidays/fragments/edit_holiday.html', context)


def edit_own_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    user = request.user
    selected_holiday = Holiday.objects.get(id=holiday_id)

    if request.method == "POST":
        form = HolidayForm(request.POST)
        data = form.data
        if selected_holiday.employee == user and selected_holiday.start_date > datetime.now().date() and selected_holiday.status < 3:
            Holiday.objects.filter(id=holiday_id).update(
                start_date=data['start_date'],
                end_date=data['end_date'],
                status=data['status'],
                note=data['note']
            )
            messages.success(request, "Holiday has been successfully updated.")
        elif selected_holiday.employee == user:
            Holiday.objects.filter(id=holiday_id).update(
                status=data['status'],
                note=data['note']
            )
            messages.success(request, "Holiday has been successfully updated.")
        else:
            messages.error(request, "Not permitted to update this absence.")
        return redirect('own_holidays')
    # GET request
    else:
        form = HolidayForm()
        if selected_holiday.employee == user and selected_holiday.start_date < datetime.now().date() and selected_holiday.status < 3:
            can_update = False
        else:
            can_update = True
        context = {
            'form': form,
            'selected_holiday': selected_holiday,
            'can_update': can_update
        }
        return render(request, 'attendance/fragments/edit_own_holiday.html', context)


def delete_holiday(request, **kwargs):
    holiday_id = kwargs['pk']
    own = None
    if 'own' in request.GET:
        own = request.GET['own']
    selected_holiday = Holiday.objects.get(id=holiday_id)
    user = request.user
    if user.role == 'A' or (selected_holiday.employee == user and selected_holiday.start_date < datetime.now().date() and selected_holiday.status < 3):
        selected_holiday.delete()
        messages.success(request, "Holiday successfully deleted.")
    if own:
        return redirect('own_holidays')
    return redirect('holidays')


def own_holidays(request):
    user = request.user
    all_entries = None
    all_entries = Holiday.objects.filter(employee=user).order_by('start_date')

    context = {
        'all_entries': all_entries
    }
    if all_entries.count() == 0:
        return HttpResponse('<h6><i class="material-icons accent-color-text left">info</i>No holidays created yet</h6>')
    return HttpResponse(render(request, 'attendance/fragments/own_holidays.html', context))


def holiday_list(request):
    data = None
    search = False

    if request.method == 'POST':
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_year = data['filter_year']
        filter_month = data['filter_month']
        filter_date = data['filter_date']
        filter_status = data['filter_status']
        if 'status' in request.GET:
            filter_status = request.GET['status']
        keyword = data['keyword']
        q_keyword = Q()
        q_status = Q()
        q_date = Q()
        q_year = Q()
        q_month = Q()

        print(filter_year)

        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | note)
        if int(filter_status) > -1:
            q_status = Q(status__exact=filter_status)
        if filter_date != '':
            q_date_start = Q(start_date__lte=filter_date)
            q_date_end = Q(end_date__gte=filter_date)
            q_date = Q(q_date_start & q_date_end)
        if filter_year != '':
            q_year = Q(Q(start_date__year=filter_year) | Q(end_date__year=filter_year))
        if int(filter_month) > 0:
            q_month = Q(Q(start_date__month=filter_month) | Q(end_date__month=filter_month))
        q = Q(q_keyword & q_status & q_date & q_year & q_month)
        entries = Holiday.objects.filter(q)
        timeline = None
        if filter_date != '':
            # get holidays 1 week before and after for timeline reference
            start = datetime.strptime(filter_date, "%Y-%m-%d") - timedelta(days=7)
            end = datetime.strptime(filter_date, "%Y-%m-%d") + timedelta(days=6)
            filter_date = datetime.strptime(filter_date, "%Y-%m-%d")
            q_date_start = Q(start_date__lte=end)
            q_date_end = Q(end_date__gte=start)
            q_date = Q(q_date_start & q_date_end)
            q = Q(q_keyword & q_status & q_date)
            timeline_entries = Holiday.objects.filter(q)

            contents = draw_calendar(start_date=start, end_date=end, center_date=filter_date,
                                     objects=timeline_entries, target='holidays')
            timeline = base64.b64encode(contents).decode()
        elif int(filter_month) > 0 and filter_year != '':
            month = int(filter_month)
            year = int(filter_year)
            # get holidays for selected month in year
            start = datetime(year=year, month=month, day=1)
            end = start + relativedelta(months=+1) - timedelta(days=1)
            q_date_start = Q(start_date__lte=end)
            q_date_end = Q(end_date__gte=start)
            q_date = Q(q_date_start & q_date_end)
            q = Q(q_keyword & q_status & q_date)
            timeline_entries = Holiday.objects.filter(q)

            contents = draw_calendar(start_date=start, end_date=end, center_date=None,
                                     objects=timeline_entries, target='holidays')
            timeline = base64.b64encode(contents).decode()
    else:
        entries = Holiday.objects.all()
        timeline = None

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data,
        'timeline': timeline
    }
    if request.method == 'POST':
        return HttpResponse(render(request, 'holidays/fragments/holiday-table.html', context))
    return HttpResponse(render(request, 'holidays/holiday_list.html', context))
