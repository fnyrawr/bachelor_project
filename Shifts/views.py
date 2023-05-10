import base64
from datetime import datetime, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Absences.models import Absence
from Availabilities.models import Availability
from Departments.models import Department
from Holidays.models import Holiday
from Qualifications.models import Qualification
from Users.models import User
from Wishes.models import Wish
from utils.create_timeline import draw_timeline
from .forms import ShiftForm, SearchForm
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

        # absences and holidays to filter out
        for employee in employees:
            if Absence.objects.filter(employee=employee, start_date__lte=date, end_date__gte=date).exists():
                employees = employees.exclude(id=employee.id)
        for employee in employees:
            if Holiday.objects.filter(employee=employee, start_date__lte=date, end_date__gte=date).exists():
                employees = employees.exclude(id=employee.id)

        # already assigned employees of this day to filter out
        for employee in employees:
            if Shift.objects.filter(employee=employee,
                                    start__year=date.year,
                                    start__month=date.month,
                                    start__day=date.day).exists():
                employees = employees.exclude(id=employee.id)

        # get availabilities and wishes for remaining
        for employee in employees:
            employee.available = None
            if Availability.objects.filter(employee=employee, weekday=weekday).exists():
                employee.available = Availability.objects.get(employee=employee, weekday=weekday)
        for employee in employees:
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
    selected_shift.delete()
    messages.success(request, "Shift successfully deleted.")
    return redirect('shifts')


def shift_list(request):
    data = None
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        keyword = data['keyword']
        q_keyword = Q()
        q_date = Q()

        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            department = Q(department__name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | department | note)
        if filter_date != '':
            q_date_start = Q(start__date__lte=filter_date)
            q_date_end = Q(end__date__gte=filter_date)
            q_date = Q(q_date_start & q_date_end)
        q = Q(q_keyword & q_date)
        entries = Shift.objects.filter(q)
        timeline = None
        if len(entries) > 0 and filter_date != '':
            contents = draw_timeline(entries, 'shifts')
            timeline = base64.b64encode(contents).decode()
    else:
        entries = Shift.objects.all()
        for entry in entries:
            qualifications = ShiftQualifications.objects.filter(shift_id=entry.id).order_by(
                'qualification__name')
            entry.qualifications = qualifications
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
    return render(request, 'shifts/shift_list.html', context)
