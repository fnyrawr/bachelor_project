import numpy
from django.shortcuts import render, redirect
import pandas as pd

from Absences.models import Absence
from Availabilities.models import Availability
from DayTemplates.models import DayTemplate, DayShiftTemplates
from Demand.models import Demand
from Holidays.models import Holiday
from Qualifications.models import Qualification
from Departments.models import Department, DepartmentQualifications
from ShiftTemplates.models import ShiftTemplate, ShiftTemplateQualifications
from Users.models import User, EmployeesQualifications
from Wishes.models import Wish
from .forms import FileForm


def data_management(request):
    context = {}
    return render(request, 'datamanagement/datamanagement.html', context)


def import_qualifications(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            for index, row in df.iterrows():
                name = row['Name']
                if row['Description'] is numpy.nan:
                    description = ''
                else:
                    description = row['Description']
                if row['Important'] == 'Yes':
                    is_important = True
                else:
                    is_important = False
                qualification = Qualification.objects.filter(name__iexact=name)
                if not qualification:
                    qualification = Qualification(
                        name=name,
                        description=description,
                        is_important=is_important
                    )
                    qualification.save()
                else:
                    qualification.update(
                        description=description,
                        is_important=is_important
                    )

            return redirect('qualifications')
        return render(request, 'datamanagement/import_qualifications.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_qualifications.html', context)


def import_departments(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            departments = pd.read_excel(data, sheet_name='Departments')
            for index, row in departments.iterrows():
                name = row['Name']
                if row['Description'] is numpy.nan:
                    description = ''
                else:
                    description = row['Description']
                department = Department.objects.filter(name__iexact=name)
                if not department:
                    department = Department(
                        name=name,
                        description=description
                    )
                    department.save()
                else:
                    department.update(description=description)
                # cleanup assigned qualifications
                department_qualifications = DepartmentQualifications.objects \
                    .filter(department__name__iexact=name)
                department_qualifications.delete()
            # import associated qualifications
            qualifications = pd.read_excel(data, sheet_name='Qualifications')
            for index, row in qualifications.iterrows():
                department = Department.objects.get(name__iexact=row['Department'])
                qualification = Qualification.objects.get(name__iexact=row['Qualification'])
                department_qualification = DepartmentQualifications(
                    department=department,
                    qualification=qualification
                )
                department_qualification.save()

            return redirect('departments')
        return render(request, 'datamanagement/import_departments.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_departments.html', context)


def import_users(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            users = pd.read_excel(data, sheet_name='Users')
            users = users.fillna('')
            for index, row in users.iterrows():
                first_name = row['First Name']
                last_name = row['Last Name']
                email = row['E-Mail']
                username = row['Username']
                staff_id = row['Staff ID']
                if row['External'] == 'Yes':
                    is_external = True
                else:
                    is_external = False
                department = Department.objects.get(name__iexact=row['Department'])
                if not department:
                    department = None
                address = row['Address']
                zip_city = (str(row['Zip']) + ' ' + row['City']).strip()
                telephone_home = row['Telephone home']
                telephone_mobile = row['Telephone mobile']
                start_contract = row['Start contract']
                end_contract = row['End contract']
                if row['Verified'] == 'Yes':
                    is_verified = True
                else:
                    is_verified = False
                if row['Role'] == 'Admin':
                    role = 'A'
                elif row['Role'] == 'Planner':
                    role = 'P'
                else:
                    role = 'E'
                if row['Active'] == 'Yes':
                    is_active = True
                else:
                    is_active = False
                work_hours = row['Work hours']
                holiday_count = row['Holiday']

                user = User.objects.filter(username__iexact=username)
                if not user:
                    user = User(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        staff_id=staff_id,
                        is_external=is_external,
                        department=department,
                        address=address,
                        zip_city=zip_city,
                        telephone_home=telephone_home,
                        telephone_mobile=telephone_mobile,
                        start_contract=start_contract,
                        end_contract=end_contract,
                        is_verified=is_verified,
                        role=role,
                        is_active=is_active,
                        work_hours=work_hours,
                        holiday_count=holiday_count
                    )
                    # set initial password
                    user.set_password('H4cKm3!fY0uC4n')
                    user.save()
                else:
                    user.update(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        staff_id=staff_id,
                        is_external=is_external,
                        department=department,
                        address=address,
                        zip_city=zip_city,
                        telephone_home=telephone_home,
                        telephone_mobile=telephone_mobile,
                        start_contract=start_contract,
                        end_contract=end_contract,
                        is_verified=is_verified,
                        role=role,
                        is_active=is_active,
                        work_hours=work_hours,
                        holiday_count=holiday_count
                    )
                # cleanup assigned qualifications
                employees_qualifications = EmployeesQualifications.objects \
                    .filter(employee__username__iexact=username)
                employees_qualifications.delete()

            # import associated qualifications
            qualifications = pd.read_excel(data, sheet_name='Qualifications')
            for index, row in qualifications.iterrows():
                employee = User.objects.get(username__iexact=row['Username'])
                qualification = Qualification.objects.get(name__iexact=row['Qualification'])
                employees_qualification = EmployeesQualifications(
                    employee=employee,
                    qualification=qualification
                )
                employees_qualification.save()

            return redirect('useraccounts')
        return render(request, 'datamanagement/import_users.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_users.html', context)


def import_absences(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            for index, row in df.iterrows():
                username = row['Username']
                start_date = row['Start Date']
                end_date = row['End Date']
                reason = row['Reason']
                status = row['Status']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                employee = User.objects.get(username__iexact=username)
                absence = Absence.objects.filter(employee=employee, start_date=start_date, end_date=end_date)
                if not absence:
                    absence = Absence(
                        employee=employee,
                        start_date=start_date,
                        end_date=end_date,
                        reason=reason,
                        status=status,
                        note=note
                    )
                    absence.save()
                else:
                    absence.update(reason=reason, status=status, note=note)

            return redirect('absences')
        return render(request, 'datamanagement/import_absences.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_absences.html', context)


def import_holidays(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            for index, row in df.iterrows():
                username = row['Username']
                start_date = row['Start Date']
                end_date = row['End Date']
                status = row['Status']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                employee = User.objects.get(username__iexact=username)
                holiday = Holiday.objects.filter(employee=employee, start_date=start_date, end_date=end_date)
                if not holiday:
                    holiday = Holiday(
                        employee=employee,
                        start_date=start_date,
                        end_date=end_date,
                        status=status,
                        note=note
                    )
                    holiday.save()
                else:
                    holiday.update(status=status, note=note)

            return redirect('holidays')
        return render(request, 'datamanagement/import_holidays.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_holidays.html', context)


def get_weekday(weekday):
    if weekday.lower() == 'monday':
        return 1
    if weekday.lower() == 'tuesday':
        return 2
    if weekday.lower() == 'wednesday':
        return 3
    if weekday.lower() == 'thursday':
        return 4
    if weekday.lower() == 'friday':
        return 5
    if weekday.lower() == 'saturday':
        return 6
    return 7


def import_demand(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            for index, row in df.iterrows():
                department = Department.objects.get(name__iexact=row['Department'])
                weekday = get_weekday(row['Weekday'])
                start_time = row['Start']
                end_time = row['End']
                staff_count = row['Staff count']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                demand = Demand.objects.filter(department=department, weekday=weekday,
                                               start_time=start_time, end_time=end_time)
                if not demand:
                    demand = Demand(
                        department=department,
                        weekday=weekday,
                        start_time=start_time,
                        end_time=end_time,
                        staff_count=staff_count,
                        note=note
                    )
                    demand.save()
                else:
                    demand.update(staff_count=staff_count, note=note)

            return redirect('demand')
        return render(request, 'datamanagement/import_demand.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_demand.html', context)


def import_availabilities(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            df['Tendency'] = df['Tendency'].fillna(0)
            for index, row in df.iterrows():
                user = User.objects.get(username__iexact=row['Username'])
                weekday = get_weekday(row['Weekday'])
                if row['Available'] == 'Yes':
                    is_available = True
                else:
                    is_available = False
                if row['Start'] is numpy.nan:
                    start_time = None
                else:
                    start_time = row['Start']
                if row['End'] is numpy.nan:
                    end_time = None
                else:
                    end_time = row['End']
                tendency = None
                if row['Tendency'] is not 0:
                    tendency = row['Tendency']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                availability = Availability.objects.filter(employee=user, weekday=weekday)
                if not availability:
                    availability = Availability(
                        employee=user,
                        weekday=weekday,
                        is_available=is_available,
                        start_time=start_time,
                        end_time=end_time,
                        tendency=tendency,
                        note=note
                    )
                    availability.save()
                else:
                    availability.update(
                        start_time=start_time,
                        end_time=end_time,
                        is_available=is_available,
                        tendency=tendency,
                        note=note
                    )

            return redirect('availabilities')
        return render(request, 'datamanagement/import_availabilities.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_availabilities.html', context)


def import_wishes(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            df = pd.read_excel(data)
            df['Tendency'] = df['Tendency'].fillna(0)
            for index, row in df.iterrows():
                user = User.objects.get(username__iexact=row['Username'])
                date = row['Date']
                if row['Available'] == 'Yes':
                    is_available = True
                else:
                    is_available = False
                if row['Start'] is numpy.nan:
                    start_time = None
                else:
                    start_time = row['Start']
                if row['End'] is numpy.nan:
                    end_time = None
                else:
                    end_time = row['End']
                tendency = None
                if row['Tendency'] is not 0:
                    tendency = row['Tendency']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                wish = Wish.objects.filter(employee=user, date=date)
                if not wish:
                    wish = Wish(
                        employee=user,
                        date=date,
                        is_available=is_available,
                        start_time=start_time,
                        end_time=end_time,
                        tendency=tendency,
                        note=note
                    )
                    wish.save()
                else:
                    wish.update(
                        start_time=start_time,
                        end_time=end_time,
                        is_available=is_available,
                        tendency=tendency,
                        note=note
                    )

            return redirect('wishes')
        return render(request, 'datamanagement/import_wishes.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_wishes.html', context)


def import_shift_templates(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            # import shifts
            shifts = pd.read_excel(data, sheet_name='Shifts')
            for index, row in shifts.iterrows():
                name = row['Name']
                department = Department.objects.get(name__iexact=row['Department'])
                start_time = row['Start']
                end_time = row['End']
                break_duration = row['Break']
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                shift_template = ShiftTemplate.objects.filter(name__iexact=name)
                if not shift_template:
                    shift_template = ShiftTemplate(
                        name=name,
                        department=department,
                        start_time=start_time,
                        end_time=end_time,
                        break_duration=break_duration,
                        note=note
                    )
                    shift_template.save()
                else:
                    shift_template.update(
                        department=department,
                        start_time=start_time,
                        end_time=end_time,
                        break_duration=break_duration,
                        note=note
                    )
                # cleanup associated qualifications
                shift_template_qualifications = ShiftTemplateQualifications.objects \
                    .filter(shift_template__name__iexact=name)
                shift_template_qualifications.delete()
            # import associated qualifications
            qualifications = pd.read_excel(data, sheet_name='Qualifications')
            for index, row in qualifications.iterrows():
                shift_template = ShiftTemplate.objects.get(name__iexact=row['Shift'])
                qualification = Qualification.objects.get(name__iexact=row['Qualification'])
                shift_template_qualification = ShiftTemplateQualifications(
                    shift_template=shift_template,
                    qualification=qualification
                )
                shift_template_qualification.save()

            return redirect('shift_templates')
        return render(request, 'datamanagement/import_shift_templates.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_shift_templates.html', context)


def import_day_templates(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            # import day templates
            day_templates = pd.read_excel(data, sheet_name='Templates')
            for index, row in day_templates.iterrows():
                name = row['Name']
                if row['Description'] is numpy.nan:
                    description = ''
                else:
                    description = row['Description']
                day_template = DayTemplate.objects.filter(name__iexact=name)
                if not day_template:
                    day_template = DayTemplate(
                        name=name,
                        description=description
                    )
                    day_template.save()
                else:
                    day_template.update(
                        description=description
                    )
                # delete assigned shifts for cleanup
                day_shift_template = DayShiftTemplates.objects \
                    .filter(day_template__name__iexact=name)
                day_shift_template.delete()
            # import assigned shifts
            shifts = pd.read_excel(data, sheet_name='Shifts')
            for index, row in shifts.iterrows():
                day_template = DayTemplate.objects.get(name__iexact=row['Template'])
                shift_template = ShiftTemplate.objects.get(name__iexact=row['Shift'])
                day_shift_template = DayShiftTemplates(
                    day_template=day_template,
                    shift_template=shift_template
                )
                day_shift_template.save()

            return redirect('day_templates')
        return render(request, 'datamanagement/import_day_templates.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_day_templates.html', context)
