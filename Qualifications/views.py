from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Departments.models import DepartmentQualifications
from Users.models import EmployeesQualifications
from .models import Qualification
from .forms import QualificationForm


class QualificationCreationView(CreateView):
    model = Qualification
    form_class = QualificationForm
    template_name = 'qualifications/create_qualification.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            qualification = form.save()
            messages.success(request, "Qualification successfully created.")
            return redirect('qualifications')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def view_qualification(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)

    associated_departments = DepartmentQualifications.objects.filter(qualification=qualification_id)\
        .order_by('department__name')
    associated_employees = EmployeesQualifications.objects.filter(qualification=qualification_id)\
        .order_by('employee__department__name', 'employee__last_name', 'employee__first_name')

    context = {
        'selected_qualification': selected_qualification,
        'associated_departments': associated_departments,
        'associated_employees': associated_employees,
    }
    return render(request, 'qualifications/qualification_detail.html', context)


def edit_qualification(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)

    if request.method == "POST":
        form = QualificationForm(request.POST)
        data = form.data
        if 'is_important' in data:
            is_important = True
        else:
            is_important = False
        Qualification.objects.filter(id=qualification_id).update(
            name=data['name'],
            description=data['description'],
            is_important=is_important
        )
        messages.success(request, "Qualification has been successfully updated.")
        return redirect('qualifications')
    # GET request
    else:
        form = QualificationForm()
        context = {'form': form, 'selected_qualification': selected_qualification}
        return render(request, 'qualifications/edit_qualification.html', context)


def delete_qualification(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)
    user = request.user
    if user.role == 'A':
        selected_qualification.delete()
        messages.success(request, "Qualification successfully deleted.")
    return redirect('qualifications')


def qualification_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Qualification.objects.order_by('name')
        for entry in all_entries:
            departments = DepartmentQualifications.objects.filter(qualification_id=entry.id).order_by(
                'department__name')
            entry.departments = departments
            employees = EmployeesQualifications.objects.filter(qualification_id=entry.id).order_by(
                'employee__last_name', 'employee__first_name')
            entry.employees = employees

    context = {'all_entries': all_entries}
    return render(request, 'qualifications/qualification_list.html', context)
