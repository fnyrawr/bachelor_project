from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Qualifications.models import Qualification
from .models import Department, DepartmentQualifications
from .forms import DepartmentForm


class DepartmentCreationView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/create_department.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, "Department successfully created.")
            return redirect('departments')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def view_department(request, **kwargs):
    department_id = kwargs['pk']
    selected_department = Department.objects.get(id=department_id)

    # import User class only here to prevent circular dependencies
    from Users.models import User, EmployeesQualifications
    associated_qualifications = DepartmentQualifications.objects.filter(department=selected_department)
    associated_employees = User.objects.filter(department=selected_department)
    work_hours = 0
    for entry in associated_employees:
        qualifications = EmployeesQualifications.objects.filter(employee=entry.id).order_by(
            'qualification__name')
        entry.qualifications = qualifications
        if entry.work_hours is not None:
            work_hours += entry.work_hours

    context = {
        'selected_department': selected_department,
        'associated_qualifications': associated_qualifications,
        'associated_employees': associated_employees,
        'associated_employees_work_hours': work_hours,
    }
    return render(request, 'departments/department_detail.html', context)


def edit_department(request, **kwargs):
    department_id = kwargs['pk']
    selected_department = Department.objects.get(id=department_id)

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        data = form.data
        Department.objects.filter(id=department_id).update(
            name=data['name'],
            description=data['description']
        )
        messages.success(request, "Department has been successfully updated.")
        return redirect('departments')
    # GET request
    else:
        associated_qualifications = DepartmentQualifications.objects.filter(department=selected_department)
        non_associated_qualifications = Qualification.objects.all().exclude(
            id__in=associated_qualifications.values('qualification'))
        form = DepartmentForm()
        context = {
            'form': form,
            'selected_department': selected_department,
            'non_associated_qualifications': non_associated_qualifications,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'departments/edit_department.html', context)


def delete_department(request, **kwargs):
    department_id = kwargs['pk']
    selected_department = Department.objects.get(id=department_id)
    user = request.user
    if user.role == 'A':
        selected_department.delete()
        messages.success(request, "Department successfully deleted.")
    return redirect('departments')


def add_qualification(request, **kwargs):
    department_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_department = Department.objects.get(id=department_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    if not DepartmentQualifications.objects\
            .filter(department=selected_department, qualification=selected_qualification).exists():
        DepartmentQualifications.objects.create(department=selected_department, qualification=selected_qualification)

    return redirect('edit_department', pk=department_id)


def remove_qualification(request, **kwargs):
    department_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_user = Department.objects.get(id=department_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    entry = DepartmentQualifications.objects.filter(department=department_id, qualification=selected_qualification)
    if entry is not None:
        entry.delete()

    return redirect('edit_department', pk=department_id)


def department_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Department.objects.order_by('name')
        # add qualifications as list to each entry
        employee_count = 0
        work_hours = 0
        for entry in all_entries:
            qualifications = DepartmentQualifications.objects.filter(department_id=entry.id).order_by(
                'qualification__name')
            entry.qualifications = qualifications
            employee_count += entry.get_employees().count()
            work_hours += entry.get_work_hours()

    context = {
        'all_entries': all_entries,
        'employee_count': employee_count,
        'work_hours': work_hours
    }
    return render(request, 'departments/department_list.html', context)
