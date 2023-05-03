from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Absence
from .forms import AbsenceForm


class AbsenceCreationView(CreateView):
    model = Absence
    form_class = AbsenceForm
    template_name = 'absences/create_absence.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            absence = form.save()
            messages.success(request, "Absence successfully created.")
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
        messages.success(request, "Absence has been successfully updated.")
        return redirect('absences')
    # GET request
    else:
        employees = User.objects.all()
        form = AbsenceForm()
        context = {
            'form': form,
            'selected_absence': selected_absence,
            'employees': employees
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
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Absence.objects.all()

    context = {
        'all_entries': all_entries
    }
    return render(request, 'absences/absence_list.html', context)
