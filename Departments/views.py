from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Department
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
        form = DepartmentForm()
        context = {'form': form, 'selected_department': selected_department}
        return render(request, 'departments/edit_department.html', context)


def delete_department(request, **kwargs):
    department_id = kwargs['pk']
    selected_department = Department.objects.get(id=department_id)
    selected_department.delete()
    messages.success(request, "Department successfully deleted.")
    return redirect('departments')


def department_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Department.objects.order_by('name')

    context = {'all_entries': all_entries}
    return render(request, 'departments/department_list.html', context)
