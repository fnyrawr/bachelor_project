from datetime import datetime, timedelta

import numpy
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
from pandas.io.formats import excel

from Absences.models import Absence
from Availabilities.models import Availability
from DayTemplates.models import DayTemplate, DayShiftTemplates
from Demand.models import Demand
from Holidays.models import Holiday
from Qualifications.models import Qualification
from Departments.models import Department, DepartmentQualifications
from ShiftTemplates.models import ShiftTemplate, ShiftTemplateQualifications
from Shifts.models import Shift
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
            df = df.fillna('')
            for index, row in df.iterrows():
                username = row['Username']
                start_date = row['Start Date']
                end_date = row['End Date']
                reason = row['Reason']
                status = row['Status']
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
            df = df.fillna('')
            for index, row in df.iterrows():
                username = row['Username']
                start_date = row['Start Date']
                end_date = row['End Date']
                status = row['Status']
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
            df = df.fillna('')
            for index, row in df.iterrows():
                department = Department.objects.get(name__iexact=row['Department'])
                weekday = get_weekday(row['Weekday'])
                start_time = row['Start']
                end_time = row['End']
                staff_count = row['Staff count']
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
            df['Note'] = df['Note'].fillna('')
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
                if row['Tendency'] != 0:
                    tendency = row['Tendency']
                else:
                    tendency = 0
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
            df['Note'] = df['Note'].fillna('')
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
                if row['Tendency'] != 0:
                    tendency = row['Tendency']
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
            shifts = shifts.fillna('')
            for index, row in shifts.iterrows():
                name = row['Name']
                department = Department.objects.get(name__iexact=row['Department'])
                start_time = row['Start']
                end_time = row['End']
                break_duration = row['Break']
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
            day_templates = day_templates.fillna('')
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


def import_shifts(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file_upload']
            # import shifts
            df = pd.read_excel(data)
            df = df.fillna('')
            for index, row in df.iterrows():
                date = str(row['Date'])
                start_time = str(row['Start'])
                end_time = str(row['End'])
                # set dates
                start = date + ' ' + start_time
                if datetime.strptime(start_time, '%H:%M:%S') < datetime.strptime(end_time, '%H:%M:%S'):
                    end = date + ' ' + end_time
                else:
                    end = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)) \
                              .strftime('%Y-%m-%d') + ' ' + end_time
                break_duration = row['Break']
                if row['Username'] is numpy.nan:
                    employee = None
                else:
                    employee = User.objects.get(username__iexact=row['Username'])
                department = Department.objects.get(name__iexact=row['Department'])
                if row['Note'] is numpy.nan:
                    note = ''
                else:
                    note = row['Note']
                if row['Highlight'] == 'Yes':
                    highlight = True
                else:
                    highlight = False
                date = datetime.strptime(date, '%Y-%m-%d')
                shift = Shift.objects.filter(employee=employee,
                                             start__year=date.year,
                                             start__month=date.month,
                                             start__day=date.day)
                if not shift:
                    shift = Shift(
                        start=start,
                        end=end,
                        break_duration=break_duration,
                        department=department,
                        employee=employee,
                        note=note,
                        highlight=highlight
                    )
                    shift.save()
                else:
                    shift.update(
                        start=start,
                        end=end,
                        break_duration=break_duration,
                        department=department,
                        employee=employee,
                        note=note,
                        highlight=highlight
                    )

            return redirect('shifts')
        return render(request, 'datamanagement/import_shifts.html', {'form': form})
    # GET request
    else:
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'datamanagement/import_shifts.html', context)


def download_exports(request):
    filename = "Exports.xlsx"
    excel.ExcelFormatter.header_style = None

    # Qualifications
    qualifications = pd.DataFrame.from_records(Qualification.objects.all().values())
    qualifications.rename(columns={
        "id": "ID",
        "name": "Name",
        "description": "Description",
        "is_important": "Important"
    }, inplace=True)
    qualifications = qualifications.set_index("ID").sort_values(by="ID")
    qualifications["Important"] = qualifications["Important"].map({True: "Yes", False: ""})

    # Departments
    departments = pd.DataFrame.from_records(Department.objects.all().values())
    departments.rename(columns={
        "id": "ID",
        "name": "Name",
        "description": "Description"
    }, inplace=True)
    departments = departments.set_index("ID").sort_values(by="ID")

    departments_qualifications = pd.DataFrame.from_records(DepartmentQualifications.objects
                                                           .values('id', 'department__name', 'qualification__name'))
    departments_qualifications.rename(columns={
        "id": "ID",
        "department__name": "Department",
        "qualification__name": "Qualification"
    }, inplace=True)
    departments_qualifications = departments_qualifications.set_index("ID").sort_values(by="ID")

    # Users
    users = pd.DataFrame.from_records(User.objects.all()
                                      .values('id',
                                              'first_name',
                                              'last_name',
                                              'email',
                                              'username',
                                              'staff_id',
                                              'is_external',
                                              'department__name',
                                              'address',
                                              'zip_city',
                                              'telephone_home',
                                              'telephone_mobile',
                                              'start_contract',
                                              'end_contract',
                                              'is_verified',
                                              'role',
                                              'is_active',
                                              'work_hours',
                                              'holiday_count'))
    users.rename(columns={
        "id": "ID",
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "E-Mail",
        "username": "Username",
        "staff_id": "Staff ID",
        "is_external": "External",
        "department__name": "Department",
        "address": "Address",
        "zip_city": "Zip city",
        "telephone_home": "Telephone home",
        "telephone_mobile": "Telephone mobile",
        "start_contract": "Start contract",
        "end_contract": "End contract",
        "is_verified": "Verified",
        "role": "Role",
        "is_active": "Active",
        "work_hours": "Work hours",
        "holiday_count": "Holiday"
    }, inplace=True)
    users = users.set_index("ID").sort_values(by="ID")
    users["External"] = users["External"].map({True: "Yes", False: ""})
    users["Verified"] = users["Verified"].map({True: "Yes", False: ""})
    users["Role"] = users["Role"].map({"A": "Admin", "P": "Planner", "E": "Employee"})
    users["Active"] = users["Active"].map({True: "Yes", False: ""})

    emp_qualifications = pd.DataFrame.from_records(EmployeesQualifications.objects
                                                   .values('id', 'employee__username', 'qualification__name'))
    emp_qualifications.rename(columns={
        "id": "ID",
        "employee__username": "Username",
        "qualification__name": "Qualification"
    }, inplace=True)
    emp_qualifications = emp_qualifications.set_index("ID").sort_values(by="ID")

    # Absences
    absences = pd.DataFrame.from_records(Absence.objects
                                         .values('id',
                                                 'employee__username',
                                                 'start_date',
                                                 'end_date',
                                                 'reason',
                                                 'status',
                                                 'note'))
    absences.rename(columns={
        "id": "ID",
        "employee__username": "Username",
        "start_date": "Start Date",
        "end_date": "End Date",
        "reason": "Reason",
        "status": "Status",
        "note": "Note"
    }, inplace=True)
    absences = absences.set_index("ID").sort_values(by="ID")

    # Holidays
    holidays = pd.DataFrame.from_records(Holiday.objects
                                         .values('id',
                                                 'employee__username',
                                                 'start_date',
                                                 'end_date',
                                                 'status',
                                                 'note'))
    holidays.rename(columns={
        "id": "ID",
        "employee__username": "Username",
        "start_date": "Start Date",
        "end_date": "End Date",
        "status": "Status",
        "note": "Note"
    }, inplace=True)
    holidays = holidays.set_index("ID").sort_values(by="ID")

    # Demand
    demand = pd.DataFrame.from_records(Demand.objects
                                       .values('id',
                                               'department__name',
                                               'weekday',
                                               'start_time',
                                               'end_time',
                                               'staff_count',
                                               'note'))
    demand.rename(columns={
        "id": "ID",
        "department__name": "Department",
        "weekday": "Weekday",
        "start_time": "Start",
        "end_time": "End",
        "staff_count": "Staff count",
        "note": "Note"
    }, inplace=True)
    demand = demand.set_index("ID").sort_values(by="ID")
    demand["Weekday"] = demand["Weekday"].map({1: "Monday",
                                               2: "Tuesday",
                                               3: "Wednesday",
                                               4: "Thursday",
                                               5: "Friday",
                                               6: "Saturday",
                                               7: "Sunday"})
    demand["Start"] = demand["Start"].astype(str).str[:5]
    demand["End"] = demand["End"].astype(str).str[:5]

    # Availabilities
    availabilities = pd.DataFrame.from_records(Availability.objects
                                               .values('id',
                                                       'employee__username',
                                                       'weekday',
                                                       'is_available',
                                                       'start_time',
                                                       'end_time',
                                                       'tendency',
                                                       'note'))
    availabilities.rename(columns={
        "id": "ID",
        "employee__username": "Username",
        "weekday": "Weekday",
        "is_available": "Available",
        "start_time": "Start",
        "end_time": "End",
        "tendency": "Tendency",
        "note": "Note"
    }, inplace=True)
    availabilities = availabilities.set_index("ID").sort_values(by="ID")
    availabilities["Available"] = availabilities["Available"].map({True: "Yes", False: ""})
    availabilities["Weekday"] = availabilities["Weekday"].map({1: "Monday",
                                                               2: "Tuesday",
                                                               3: "Wednesday",
                                                               4: "Thursday",
                                                               5: "Friday",
                                                               6: "Saturday",
                                                               7: "Sunday"})
    availabilities["Start"] = availabilities["Start"].astype(str).str[:5]
    availabilities["End"] = availabilities["End"].astype(str).str[:5]
    availabilities["Start"] = availabilities.apply(lambda x: x["Start"] if x["Start"] != "None" else "", axis=1)
    availabilities["End"] = availabilities.apply(lambda x: x["End"] if x["End"] != "None" else "", axis=1)

    # Wishes
    wishes = pd.DataFrame.from_records(Wish.objects
                                       .values('id',
                                               'employee__username',
                                               'date',
                                               'is_available',
                                               'start_time',
                                               'end_time',
                                               'tendency',
                                               'note'))
    wishes.rename(columns={
        "id": "ID",
        "employee__username": "Username",
        "date": "Date",
        "is_available": "Available",
        "start_time": "Start",
        "end_time": "End",
        "tendency": "Tendency",
        "note": "Note"
    }, inplace=True)
    wishes = wishes.set_index("ID").sort_values(by="ID")
    wishes["Available"] = wishes["Available"].map({True: "Yes", False: ""})
    wishes["Start"] = wishes["Start"].astype(str).str[:5]
    wishes["End"] = wishes["End"].astype(str).str[:5]
    wishes["Start"] = wishes.apply(lambda x: x["Start"] if x["Start"] != "None" else "", axis=1)
    wishes["End"] = wishes.apply(lambda x: x["End"] if x["End"] != "None" else "", axis=1)

    # ShiftTemplates
    shift_templates = pd.DataFrame.from_records(ShiftTemplate.objects
                                                .values('id',
                                                        'name',
                                                        'department__name',
                                                        'start_time',
                                                        'end_time',
                                                        'break_duration',
                                                        'note'))
    shift_templates.rename(columns={
        "id": "ID",
        "name": "Name",
        "department__name": "Department",
        "start_time": "Start",
        "end_time": "End",
        "break_duration": "Break",
        "note": "Note"
    }, inplace=True)
    shift_templates = shift_templates.set_index("ID").sort_values(by="ID")
    shift_templates["Start"] = shift_templates["Start"].astype(str).str[:5]
    shift_templates["End"] = shift_templates["End"].astype(str).str[:5]
    shift_templates["Break"] = shift_templates["Break"].astype(str).str[:5]

    st_qualifications = pd.DataFrame.from_records(ShiftTemplateQualifications.objects
                                                  .values('id', 'shift_template__name', 'qualification__name'))
    st_qualifications.rename(columns={
        "id": "ID",
        "shift_template__name": "Shift",
        "qualification__name": "Qualification"
    }, inplace=True)
    st_qualifications = st_qualifications.set_index("ID").sort_values(by="ID")

    # DayTemplates
    day_templates = pd.DataFrame.from_records(DayTemplate.objects
                                              .values('id',
                                                      'name',
                                                      'description'))
    day_templates.rename(columns={
        "id": "ID",
        "name": "Name",
        "description": "Description"
    }, inplace=True)
    day_templates = day_templates.set_index("ID").sort_values(by="ID")

    day_shift_templates = pd.DataFrame.from_records(DayShiftTemplates.objects
                                                    .values('id', 'day_template__name', 'shift_template__name'))
    day_shift_templates.rename(columns={
        "id": "ID",
        "day_template__name": "Template",
        "shift_template__name": "Shift"
    }, inplace=True)
    day_shift_templates = day_shift_templates.set_index("ID").sort_values(by="ID")

    # Shifts
    shifts_df = pd.DataFrame.from_records(Shift.objects.all()
                                          .values('id',
                                                  'start',
                                                  'end',
                                                  'employee__username',
                                                  'department__name',
                                                  'highlight',
                                                  'note'))
    shifts = pd.DataFrame()
    shifts['ID'] = shifts_df['id']
    shifts['Date'] = shifts_df['start'].astype(str).str[:10]
    shifts['Start'] = shifts_df['start'].astype(str).str[11:16]
    shifts['End'] = shifts_df['end'].astype(str).str[11:16]
    shifts['Username'] = shifts_df['employee__username']
    shifts['Department'] = shifts_df['department__name']
    shifts['Highlight'] = shifts_df['highlight'].map({True: "Yes", False: ""})
    shifts['Note'] = shifts_df['note']
    shifts = shifts.set_index("ID").sort_values(by="ID")

    # write to .xlsx
    with pd.ExcelWriter(filename) as writer:
        qualifications.to_excel(writer, sheet_name="Qualifications")
        departments.to_excel(writer, sheet_name="Departments")
        departments_qualifications.to_excel(writer, sheet_name="DepartmentQualifications")
        users.to_excel(writer, sheet_name="Users")
        emp_qualifications.to_excel(writer, sheet_name="EmployeesQualifications")
        absences.to_excel(writer, sheet_name="Absences")
        holidays.to_excel(writer, sheet_name="Holidays")
        demand.to_excel(writer, sheet_name="Demand")
        availabilities.to_excel(writer, sheet_name="Availabilities")
        wishes.to_excel(writer, sheet_name="Wishes")
        shift_templates.to_excel(writer, sheet_name="ShiftTemplates")
        st_qualifications.to_excel(writer, sheet_name="ShiftTemplateQualifications")
        day_templates.to_excel(writer, sheet_name="DayTemplates")
        day_shift_templates.to_excel(writer, sheet_name="DayTemplateShifts")
        shifts.to_excel(writer, sheet_name="Shifts")

    with open(filename, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=/media/generated/' + filename
    return response
