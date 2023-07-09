import base64
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Shifts.models import Shift, ShiftQualifications
from Users.models import User
from utils.create_calendar import draw_calendar
from .models import Absence
from .forms import AbsenceForm, SearchForm


class AbsenceCreationView(CreateView):
    model = Absence
    form_class = AbsenceForm
    template_name = 'absences/create_absence.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            absence = form.save()
            messages.success(request, "Absence successfully created.")

            # unassign employee from conflicting shifts
            selected_absence = absence
            if selected_absence.status == 3:
                q_employee = Q(employee=selected_absence.employee)
                q_date_start = Q(start__gte=selected_absence.start_date)
                q_date_end = Q(start__lte=selected_absence.end_date)
                emp_name = selected_absence.employee.first_name + ' ' + selected_absence.employee.last_name
                Shift.objects.filter(Q(q_employee & q_date_start & q_date_end)).update(
                    employee_id=None,
                    highlight=True,
                    note=emp_name + ' is absent'
                )
                messages.info(request, "Unassigned employee from conflicting shifts.")

            return redirect('absences')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


class OwnAbsenceCreationView(CreateView):
    model = Absence
    form_class = AbsenceForm
    template_name = 'absences/add_own_absence.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            absence = form.save()
            messages.success(request, "Absence successfully created.")

            return redirect('own_absences')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def edit_absence(request, **kwargs):
    absence_id = kwargs['pk']
    selected_absence = Absence.objects.get(id=absence_id)

    # filter conflicting shifts
    q_employee = Q(employee=selected_absence.employee)
    q_date_start = Q(start__gte=selected_absence.start_date)
    q_date_end = Q(start__lte=selected_absence.end_date)
    conflicting_shifts = Shift.objects.filter(Q(q_employee & q_date_start & q_date_end))
    for shift in conflicting_shifts:
        qualifications = ShiftQualifications.objects.filter(shift_id=shift.id).order_by(
            'qualification__name')
        shift.qualifications = qualifications

    if request.method == "POST":
        form = AbsenceForm(request.POST)
        data = form.data
        Absence.objects.filter(id=absence_id).update(
            employee=data['employee'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            reason=data['reason'],
            status=data['status'],
            note=data['note']
        )

        # unassign employee from conflicting shifts
        selected_absence = Absence.objects.get(id=absence_id)
        if selected_absence.status == 3:
            q_employee = Q(employee=selected_absence.employee)
            q_date_start = Q(start__gte=selected_absence.start_date)
            q_date_end = Q(start__lte=selected_absence.end_date)
            emp_name = selected_absence.employee.first_name + ' ' + selected_absence.employee.last_name
            Shift.objects.filter(Q(q_employee & q_date_start & q_date_end)).update(
                employee_id=None,
                highlight=True,
                note=emp_name + ' is absent'
            )
            messages.info(request, "Unassigned employee from conflicting shifts.")

        messages.success(request, "Absence has been successfully updated.")
        return redirect('absences')
    # GET request
    else:
        employees = User.objects.all()
        form = AbsenceForm()
        context = {
            'form': form,
            'selected_absence': selected_absence,
            'employees': employees,
            'conflicting_shifts': conflicting_shifts
        }
        return render(request, 'absences/edit_absence.html', context)


def edit_own_absence(request, **kwargs):
    absence_id = kwargs['pk']
    selected_absence = Absence.objects.get(id=absence_id)

    if request.method == "POST":
        form = AbsenceForm(request.POST)
        data = form.data
        Absence.objects.filter(id=absence_id).update(
            status=data['status'],
            note=data['note']
        )
        messages.success(request, "Absence has been successfully updated.")
        return redirect('own_absences')
    # GET request
    else:
        form = AbsenceForm()
        context = {
            'form': form,
            'selected_absence': selected_absence
        }
        return render(request, 'absences/edit_own_absence.html', context)


def delete_absence(request, **kwargs):
    absence_id = kwargs['pk']
    selected_absence = Absence.objects.get(id=absence_id)
    selected_absence.delete()
    messages.success(request, "Absence successfully deleted.")
    return redirect('absences')


def own_absences(request):
    user = request.user
    all_entries = None
    all_entries = Absence.objects.filter(employee=user).order_by('start_date')

    context = {
        'all_entries': all_entries
    }
    return render(request, 'absences/own_absences.html', context)


def absence_list(request):
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
        filter_reason = data['filter_reason']
        keyword = data['keyword']
        q_keyword = Q()
        q_status = Q()
        q_reason = Q()
        q_date = Q()
        q_year = Q()
        q_month = Q()

        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | note)
        if int(filter_status) > -1:
            q_status = Q(status__exact=filter_status)
        if int(filter_reason) > -1:
            q_status = Q(reason__exact=filter_reason)
        if filter_date != '':
            q_date_start = Q(start_date__lte=filter_date)
            q_date_end = Q(end_date__gte=filter_date)
            q_date = Q(q_date_start & q_date_end)
        if filter_year != '':
            q_year = Q(Q(start_date__year=filter_year) | Q(end_date__year=filter_year))
        if int(filter_month) > 0:
            q_month = Q(Q(start_date__month=filter_month) | Q(end_date__month=filter_month))
        q = Q(q_keyword & q_status & q_date & q_reason & q_year & q_month)
        entries = Absence.objects.filter(q)

        timeline = None
        if filter_date != '':
            # get holidays 1 week before and after for timeline reference
            start = datetime.strptime(filter_date, "%Y-%m-%d") - timedelta(days=7)
            end = datetime.strptime(filter_date, "%Y-%m-%d") + timedelta(days=6)
            q_date_start = Q(start_date__lte=end)
            q_date_end = Q(end_date__gte=start)
            q_date = Q(q_date_start & q_date_end)
            q = Q(q_keyword & q_status & q_date)
            timeline_entries = Absence.objects.filter(q)

            contents = draw_calendar(start_date=start, end_date=end, center_date=filter_date,
                                     objects=timeline_entries, target='absences')
            timeline = base64.b64encode(contents).decode()
        elif int(filter_month) > 0 and filter_year != '':
            month = int(filter_month)
            year = int(filter_year)
            # get absences for selected month in year
            start = datetime(year=year, month=month, day=1)
            end = start + relativedelta(months=+1) - timedelta(days=1)
            q_date_start = Q(start_date__lte=end)
            q_date_end = Q(end_date__gte=start)
            q_date = Q(q_date_start & q_date_end)
            q = Q(q_keyword & q_status & q_date)
            timeline_entries = Absence.objects.filter(q)

            contents = draw_calendar(start_date=start, end_date=end, center_date=None,
                                     objects=timeline_entries, target='absences')
            timeline = base64.b64encode(contents).decode()
    else:
        entries = Absence.objects.all()
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
    return render(request, 'absences/absence_list.html', context)
