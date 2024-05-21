import base64
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import chain

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Absences.models import Absence
from Availabilities.models import Availability
from Demand.models import Demand
from Departments.models import Department, DepartmentQualifications
from Holidays.models import Holiday
from Qualifications.models import Qualification
from Users.models import User
from Wishes.models import Wish
from utils.create_shiftplan import draw_shiftplan
from utils.create_timeline import draw_timeline, time_to_dec
from .forms import ShiftForm, SearchForm, WorkHoursSearchForm, ShiftplanSearchForm
from .models import Shift, ShiftQualifications


class ShiftCreationView(CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'shifts/create_shift.html'

    def post(self, request):
        # merge date and time before form validation
        data = request.POST
        data._mutable = True
        data['start'] = data['date'] + ' ' + data['start_time']
        if datetime.strptime(data['start_time'], '%H:%M') < datetime.strptime(data['end_time'], '%H:%M'):
            data['end'] = data['date'] + ' ' + data['end_time']
        else:
            data['end'] = (datetime.strptime(data['date'], '%Y-%m-%d') + timedelta(days=1)) \
                              .strftime('%Y-%m-%d') + ' ' + data['end_time']
        data._mutable = False
        form = self.form_class(data=data)
        if form.is_valid():
            shift = form.save()
            if 'highlight' in data:
                Shift.objects.filter(id=shift.id).update(highlight=True)
            # get department qualifications and add them to created shift
            dep_qualifications = DepartmentQualifications.objects.filter(department=shift.department)
            for dq in dep_qualifications:
                sq = ShiftQualifications(shift=shift, qualification=dq.qualification)
                sq.save()
            messages.success(request, "Shift successfully created.")
            return redirect('shifts')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def add_qualification(request, **kwargs):
    shift_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_shift = Shift.objects.get(id=shift_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    if not ShiftQualifications.objects \
            .filter(shift=shift_id, qualification=qualification_id).exists():
        ShiftQualifications.objects.create(shift=selected_shift,
                                           qualification=selected_qualification)

    return redirect('edit_shift', pk=shift_id)


def remove_qualification(request, **kwargs):
    shift_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    entry = ShiftQualifications.objects.filter(shift=shift_id,
                                               qualification=qualification_id)
    if entry is not None:
        entry.delete()

    return redirect('edit_shift', pk=shift_id)


def edit_shift(request, **kwargs):
    shift_id = kwargs['pk']
    selected_shift = Shift.objects.get(id=shift_id)

    if request.method == "POST":
        # merge date and time before form validation
        post_data = request.POST
        post_data._mutable = True
        post_data['start'] = post_data['date'] + ' ' + post_data['start_time']
        if datetime.strptime(post_data['start_time'], '%H:%M') < datetime.strptime(post_data['end_time'], '%H:%M'):
            post_data['end'] = post_data['date'] + ' ' + post_data['end_time']
        else:
            post_data['end'] = (datetime.strptime(post_data['date'], '%Y-%m-%d') + timedelta(days=1)) \
                                   .strftime('%Y-%m-%d') + ' ' + post_data['end_time']
        post_data._mutable = False

        form = ShiftForm(post_data)
        data = form.data
        print(data)
        if data['note'] != '':
            note = data['note']
        else:
            note = ''
        if 'highlight' in data:
            highlight = True
        else:
            highlight = False
        Shift.objects.filter(id=shift_id).update(
            department=data['department'],
            employee=data['employee'],
            start=data['start'],
            end=data['end'],
            break_duration=data['break_duration'],
            note=note,
            highlight=highlight
        )
        messages.success(request, "Shift has been successfully updated.")
        return redirect('shifts')
    # GET request
    else:
        weekday = selected_shift.start.weekday() + 1
        date = selected_shift.start
        associated_qualifications = ShiftQualifications.objects.filter(shift=selected_shift)
        non_associated_qualifications = Qualification.objects.all().exclude(
            id__in=associated_qualifications.values('qualification'))
        departments = Department.objects.all()
        employees = User.objects.all()

        # filter out employees missing qualifications
        shift_qualifications = selected_shift.get_qualifications()

        for employee in employees:
            # filter out employees missing qualifications
            employee_qualifications = employee.get_qualifications()
            for sq in shift_qualifications:
                if sq.qualification.is_important:
                    match = False
                    for eq in employee_qualifications:
                        if sq.qualification.id == eq.qualification.id:
                            match = True
                    if not match:
                        employees = employees.exclude(id=employee.id)

            # absences and holidays to filter out
            if Absence.objects.filter(employee=employee, start_date__lte=date, end_date__gte=date).exists():
                employees = employees.exclude(id=employee.id)
            if Holiday.objects.filter(employee=employee, start_date__lte=date, end_date__gte=date).exists():
                employees = employees.exclude(id=employee.id)
            # filter out unavailable without explicit shift wish
            if Availability.objects.filter(employee=employee, weekday=weekday, is_available=False).exists():
                if not Wish.objects.filter(employee=employee, date=date, is_available=True).exists():
                    employees = employees.exclude(id=employee.id)
            # already assigned employees of this day to filter out
            if Shift.objects.filter(employee=employee,
                                    start__year=date.year,
                                    start__month=date.month,
                                    start__day=date.day).exists():
                employees = employees.exclude(id=employee.id)

        emp_in_department = employees.filter(Q(department__id=selected_shift.department.id))
        emp_other_department = employees.filter(~Q(department__id=selected_shift.department.id))
        employees = list(emp_in_department) + list(emp_other_department)

        # get availabilities and wishes for remaining
        for employee in employees:
            employee.available = None
            if Availability.objects.filter(employee=employee, weekday=weekday).exists():
                employee.available = Availability.objects.get(employee=employee, weekday=weekday)
            employee.wish = None
            if Wish.objects.filter(employee=employee, date=date).exists():
                employee.wish = Wish.objects.get(employee=employee, date=date)

        form = ShiftForm()
        context = {
            'form': form,
            'selected_shift': selected_shift,
            'departments': departments,
            'employees': employees,
            'non_associated_qualifications': non_associated_qualifications,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'shifts/edit_shift.html', context)


def assign_employee(request, **kwargs):
    shift_id = kwargs['pk1']
    employee_id = kwargs['pk2']

    Shift.objects.filter(id=shift_id).update(employee=employee_id)
    return redirect('edit_shift', pk=shift_id)


def remove_employee(request, **kwargs):
    shift_id = kwargs['pk']

    Shift.objects.filter(id=shift_id).update(employee=None)
    return redirect('edit_shift', pk=shift_id)


def delete_shift(request, **kwargs):
    shift_id = kwargs['pk']
    selected_shift = Shift.objects.get(id=shift_id)
    user = request.user
    if user.role == 'A' or user.role == 'E':
        selected_shift.delete()
        messages.success(request, "Shift successfully deleted.")
    return redirect('shifts')


class Week:
    def __init__(self, name, start, end, shift_count, work_hours):
        self.name = name
        self.start = start
        self.end = end
        self.shift_count = shift_count
        self.work_hours = work_hours


def work_hours(request):
    data = None
    search = False
    weeks = []
    shift_count_total = 0
    work_hours_total = 0
    target_hours = 0
    employee = request.user

    if request.method == "POST":
        search = True
        searchForm = WorkHoursSearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        count_weeks = int(data['count_weeks'])
        employee_id = data['employee']
        if employee_id != '' and int(employee_id) > 0:
            employee = User.objects.get(id=employee_id)

            if filter_date == '':
                start_day = datetime.today().date()
            else:
                start_day = datetime.strptime(filter_date, "%Y-%m-%d")
            weekday_idx = start_day.weekday()

            # overview work hours last n weeks for employee
            filter_start = start_day - timedelta(days=weekday_idx)
            filter_end = start_day + timedelta(days=6-weekday_idx)
            shift_count_total = 0
            work_hours_total = 0
            weeks = []
            for i in range(count_weeks):
                shifts = Shift.objects.filter(employee=employee, start__gte=filter_start, start__lte=filter_end)
                hours = 0
                shift_count = 0
                for shift in shifts:
                    shift_count += 1
                    hours += time_to_dec(shift.get_work_hours())
                week = Week(name='Week ' + str(filter_start.isocalendar().week), start=filter_start, end=filter_end,
                            shift_count=shift_count, work_hours=hours)
                weeks.append(week)
                shift_count_total += shift_count
                work_hours_total += hours
                filter_start -= timedelta(days=7)
                filter_end -= timedelta(days=7)
            if employee.work_hours is not None:
                target_hours = count_weeks*employee.work_hours
            else:
                target_hours = None
    employees = User.objects.all()

    context = {
        'weeks': weeks,
        'shift_count_total': shift_count_total,
        'work_hours_total': work_hours_total,
        'target_hours': target_hours,
        'employee': employee,
        'employees': employees,
        'search': search,
        'form': WorkHoursSearchForm,
        'data': data
    }
    return render(request, 'shifts/work_hours.html', context)


def own_shifts(request):
    data = None
    search = False
    user = request.user
    timeline_upcoming = None
    timeline_recent = None

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        keyword = data['keyword']
        q_keyword = Q()
        q_date = Q()
        q_employee = Q(employee=request.user)

        if keyword != '':
            department = Q(department__name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(department | note)
        if filter_date != '':
            fd = datetime.strptime(filter_date, "%Y-%m-%d")
            wd = fd.weekday()
            filter_start = fd - timedelta(days=wd)
            filter_end = fd + timedelta(days=6 - wd)
            q_date_start = Q(start__date__gte=filter_start)
            q_date_end = Q(start__date__lte=filter_end)
            q_date = Q(q_date_start & q_date_end)

        q = Q(q_keyword & q_date & q_employee)
        entries = Shift.objects.filter(q)

        # setting not needed attributes none
        recent_shifts = None
        upcoming_shifts = None
        weeks = None
        shift_count_total = None
        work_hours_total = None
        target_hours = None

        if len(entries) > 0 and keyword == '':
            contents = draw_timeline(entries, 'shifts_listed')
            timeline_recent = base64.b64encode(contents).decode()

        paginator = Paginator(entries, per_page=10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        page_obj = None
        today = datetime.today().date()
        d_today = today.weekday()
        # recent and upcoming shifts
        filter_start = today - timedelta(days=7+d_today)
        filter_end = today
        recent_shifts = Shift.objects.filter(employee=user, start__gte=filter_start, start__lte=filter_end)
        recent_shifts.filter_start = filter_start
        recent_shifts.filter_end = filter_end
        filter_start = today
        filter_end = today + timedelta(days=13-d_today)
        upcoming_shifts = Shift.objects.filter(employee=user, start__gte=filter_start, start__lte=filter_end)
        upcoming_shifts.filter_start = filter_start
        upcoming_shifts.filter_end = filter_end
        entries = upcoming_shifts

        # overview work hours last 12 weeks
        filter_start = today + timedelta(days=7-d_today)
        filter_end = today + timedelta(days=14-d_today)
        shift_count_total = 0
        work_hours_total = 0
        weeks = []
        week_count = 10
        for i in range(week_count):
            shifts = Shift.objects.filter(employee=user, start__gte=filter_start, start__lt=filter_end)
            hours = 0
            shift_count = 0
            for shift in shifts:
                shift_count += 1
                hours += time_to_dec(shift.get_work_hours())
            week = Week(name='Week ' + str(filter_start.isocalendar().week), start=filter_start, end=filter_end,
                        shift_count=shift_count, work_hours=hours)
            weeks.append(week)
            shift_count_total += shift_count
            work_hours_total += hours
            filter_start -= timedelta(days=7)
            filter_end -= timedelta(days=7)
        if user.work_hours:
            target_hours = week_count*user.work_hours
        else:
            target_hours = 0

        # timelines upcoming and recent shifts
        if len(upcoming_shifts) > 0:
            contents = draw_timeline(upcoming_shifts, 'shifts_listed')
            timeline_upcoming = base64.b64encode(contents).decode()
        if len(recent_shifts) > 0:
            contents = draw_timeline(recent_shifts, 'shifts_listed')
            timeline_recent = base64.b64encode(contents).decode()

    context = {
        'page_obj': page_obj,
        'recent_shifts': recent_shifts,
        'upcoming_shifts': upcoming_shifts,
        'weeks': weeks,
        'shift_count_total': shift_count_total,
        'work_hours_total': work_hours_total,
        'target_hours': target_hours,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data,
        'timeline_upcoming': timeline_upcoming,
        'timeline_recent': timeline_recent
    }
    return render(request, 'shifts/own_shifts.html', context)


def shift_list(request):
    search = False
    demand = None
    keyword = None

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        keyword = data['keyword']

        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            department = Q(department__name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | department | note)
        else:
            q_keyword = Q()
        if filter_date != '':
            q_date_start = Q(start__date__lte=filter_date)
            q_date_end = Q(end__date__gte=filter_date)
            q_date = Q(q_date_start & q_date_end)
        else:
            q_date = Q()
        q = Q(q_keyword & q_date)
        entries = Shift.objects.filter(q).order_by('department__name')
        timeline = None
        if len(entries) > 0 and filter_date != '':
            contents = draw_timeline(entries, 'shifts_filtered')
            timeline = base64.b64encode(contents).decode()
    else:
        filter_date = datetime.today().strftime('%Y-%m-%d')
        searchForm = SearchForm()
        data = searchForm.data
        data['filter_date'] = filter_date
        q_date_start = Q(start__date__lte=filter_date)
        q_date_end = Q(end__date__gte=filter_date)
        q_date = Q(q_date_start & q_date_end)
        entries = Shift.objects.filter(q_date).order_by('department__name')
        for entry in entries:
            qualifications = ShiftQualifications.objects.filter(shift_id=entry.id).order_by('qualification__name')
            entry.qualifications = qualifications
        timeline = None
        if len(entries) > 0:
            contents = draw_timeline(entries, 'shifts_filtered')
            timeline = base64.b64encode(contents).decode()

    # get demand for day
    if filter_date is not None:
        weekday = datetime.strptime(filter_date, '%Y-%m-%d').weekday()+1
        if keyword is not None:
            q_keyword = Q(department__name__icontains=keyword)
        else:
            q_keyword = Q()
        q_weekday = Q(weekday=weekday)
        q_filter = Q(q_weekday & q_keyword)
        demand_entries = Demand.objects.filter(q_filter).order_by('department__name', 'start_time', 'end_time')
        if len(demand_entries) > 0:
            contents = draw_timeline(demand_entries, 'demand_listed')
            demand = base64.b64encode(contents).decode()

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data,
        'timeline': timeline,
        'demand': demand
    }
    return render(request, 'shifts/shift_list.html', context)


@dataclass
class DayEntry:
    etype: str
    employee: User = None
    shift: Shift = None
    department: Department = None


def shiftplan(request, **kwargs):
    data = None
    search = False
    timeline = None
    employees = None
    all_entries = None

    if request.method == "POST":
        search = True
        searchForm = ShiftplanSearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        department_id = data['department']

        if department_id != '' and int(department_id) > 0:
            department = Department.objects.get(id=department_id)

            if filter_date == '':
                start_day = datetime.today().date()
            else:
                start_day = datetime.strptime(filter_date, "%Y-%m-%d")
            weekday_idx = start_day.weekday()
            week_start = start_day - timedelta(days=weekday_idx)
            week_end = start_day + timedelta(days=6-weekday_idx)

            # get employees from department or with shifts in department
            q_emp_ids_from_department = User.objects.filter(department=department).values_list('id', flat=True)
            q_emp_ids_from_shifts = Shift.objects.filter(start__date__gte=week_start, start__date__lte=week_end,
                                                         department=department).values_list('employee', flat=True)
            # merge results in distinct list
            q_emp_ids = list(set(chain(q_emp_ids_from_department, q_emp_ids_from_shifts)))
            # get all employees from that list
            employees = User.objects.filter(id__in=q_emp_ids, is_active=True)\
                .order_by('last_name', 'first_name', 'department')

            # iterate over days to find the maximum row length (employees + max_unassigned_shifts)
            i_day = week_start
            max_unassigned_shifts = 0
            for i in range(7):
                unassigned_shifts = Shift.objects.filter(employee__isnull=True, department=department,
                                                         start__date=i_day)
                if len(unassigned_shifts) > max_unassigned_shifts:
                    max_unassigned_shifts = len(unassigned_shifts)
                i_day += timedelta(days=1)

            # get this weeks work hours for each employee
            i_day = week_start
            for employee in employees:
                week_work_hours = 0
                shifts = Shift.objects.filter(employee=employee, start__date__gte=i_day,
                                              end__date__lte=i_day+timedelta(days=7))
                for shift in shifts:
                    week_work_hours += time_to_dec(shift.get_work_hours())
                employee.week_work_hours = week_work_hours

            # two dimensional array for entries
            row_count = len(employees) + max_unassigned_shifts
            all_entries = []

            i_day += timedelta(days=1)

            # write entries in array while iterating over days
            i_day = week_start
            for i in range(7):
                # reserve 0 for the actual date
                row = [i_day]
                j = 1
                for employee in employees:
                    # get absences
                    absence = Absence.objects.filter(employee=employee,
                                                     start_date__lte=i_day,
                                                     end_date__gte=i_day,
                                                     status=3)
                    if absence.exists():
                        entry = DayEntry(etype='Absent', employee=employee)
                    else:
                        # get holidays
                        holiday = Holiday.objects.filter(employee=employee,
                                                         start_date__lte=i_day,
                                                         end_date__gte=i_day,
                                                         status=3)
                        if holiday.exists():
                            entry = DayEntry(etype='Holiday', employee=employee)
                        else:
                            # get shift
                            shift = Shift.objects.filter(employee=employee, start__date=i_day)
                            if shift.exists():
                                shift = shift.get()
                                entry = DayEntry(etype='Shift', employee=employee, department=department, shift=shift)
                            else:
                                entry = DayEntry(etype='None', employee=employee)
                    row.append(entry)
                    j += 1
                # append unassigned shifts at the bottom
                unassigned_shifts = Shift.objects.filter(employee__isnull=True, department=department, start__date=i_day)
                for shift in unassigned_shifts:
                    entry = DayEntry(etype='Shift', department=department, shift=shift)
                    row.append(entry)
                    j += 1
                while j < row_count+1:
                    entry = DayEntry(etype='None')
                    row.append(entry)
                    j += 1
                i_day += timedelta(days=1)
                all_entries.append(row)

    if all_entries is not None:
        department = Department.objects.get(id=department_id)
        if 'create_pdf' in request.POST:
            # create PDF
            filename = 'Shiftplan_' + department.name + (all_entries[0][0]).strftime("_Week_%W") + '.pdf'
            pdf_file = draw_shiftplan(all_entries, department, 'pdf')
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=/media/generated/' + filename
            return response
        else:
            # create preview
            contents = draw_shiftplan(all_entries, department, 'web')
            timeline = base64.b64encode(contents).decode()

    departments = Department.objects.all()
    context = {
        'search': search,
        'form': ShiftplanSearchForm,
        'data': data,
        'employees': employees,
        'departments': departments,
        'entries': all_entries,
        'timeline': timeline,
    }
    return render(request, 'shifts/shiftplan.html', context)


# HTMX
def search_own_shifts(request):
    filter_date = request.POST.get('filter_date')
    keyword = request.POST.get('keyword')
    q_keyword = Q()
    q_date = Q()
    q_employee = Q(employee=request.user)

    if keyword is not None and keyword != '':
        department = Q(department__name__icontains=keyword)
        note = Q(note__icontains=keyword)
        q_keyword = Q(department | note)
    if filter_date is not None and filter_date != '':
        fd = datetime.strptime(filter_date, "%Y-%m-%d")
        wd = fd.weekday()
        filter_start = fd - timedelta(days=wd)
        filter_end = fd + timedelta(days=6 - wd)
        q_date_start = Q(start__date__gte=filter_start)
        q_date_end = Q(start__date__lte=filter_end)
        q_date = Q(q_date_start & q_date_end)

    q = Q(q_keyword & q_date & q_employee)
    entries = Shift.objects.filter(q)

    timeline_recent = None
    if len(entries) > 0 and filter_date != '' and keyword == '':
        contents = draw_timeline(entries, 'shifts_listed')
        timeline_recent = base64.b64encode(contents).decode()

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'count_entries': entries.count(),
        'page_obj': page_obj,
        'form': SearchForm,
        'entries': entries.count(),
        'timeline_recent': timeline_recent
    }

    if entries.count() == 0:
        return HttpResponse('<h6><i class="material-icons accent-color-text left">info</i>No shifts matching your search</h6>')
    return HttpResponse(render(request, 'shifts/fragments/own_shifts_search.html', context))
