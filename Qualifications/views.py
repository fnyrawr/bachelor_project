from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Departments.models import DepartmentQualifications
from Users.models import EmployeesQualifications
from .models import Qualification
from .forms import QualificationForm, SearchForm


class QualificationCreationView(CreateView):
    model = Qualification
    form_class = QualificationForm
    template_name = 'qualifications/fragments/create_qualification.html'

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


def view_qualification_departments(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)

    associated_departments = DepartmentQualifications.objects.filter(qualification=qualification_id)\
        .order_by('department__name')

    context = {
        'selected_qualification': selected_qualification,
        'associated_departments': associated_departments
    }
    return HttpResponse(render(request, 'qualifications/fragments/qualification_departments.html', context))


def view_qualification_employees(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)

    associated_employees = EmployeesQualifications.objects.filter(qualification=qualification_id)\
        .order_by('employee__department__name', 'employee__last_name', 'employee__first_name')

    context = {
        'selected_qualification': selected_qualification,
        'associated_employees': associated_employees
    }
    return HttpResponse(render(request, 'qualifications/fragments/qualification_employees.html', context))


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
        return HttpResponse(render(request, 'qualifications/fragments/edit_qualification.html', context))


def delete_qualification(request, **kwargs):
    qualification_id = kwargs['pk']
    selected_qualification = Qualification.objects.get(id=qualification_id)
    user = request.user
    if user.role == 'A':
        selected_qualification.delete()
        messages.success(request, "Qualification successfully deleted.")
    return redirect('qualifications')


def qualification_list(request):
    if request.method == "POST":
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        keyword = data['keyword']
        q_name = Q(name__icontains=keyword)
        q_description = Q(description__icontains=keyword)
        q = Q(q_name | q_description)
        entries = Qualification.objects.filter(q)
    else:
        entries = Qualification.objects.order_by('name')

    for entry in entries:
        departments = DepartmentQualifications.objects.filter(qualification_id=entry.id).order_by(
            'department__name')
        entry.departments = departments
        employees = EmployeesQualifications.objects.filter(qualification_id=entry.id).order_by(
            'employee__last_name', 'employee__first_name')
        entry.employees = employees

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'entries': entries
    }
    if request.method == "POST":
        return HttpResponse(render(request, 'qualifications/fragments/qualification_table.html', context))
    return HttpResponse(render(request, 'qualifications/qualification_list.html', context))
