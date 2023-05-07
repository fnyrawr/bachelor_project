from datetime import datetime, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Departments.models import Department
from Qualifications.models import Qualification
from Users.models import User
from .forms import ShiftForm
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
            data['end'] = (datetime.strptime(data['date'], '%Y-%m-%d') + timedelta(days=1))\
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
        associated_qualifications = ShiftQualifications.objects.filter(shift=selected_shift)
        non_associated_qualifications = Qualification.objects.all().exclude(
            id__in=associated_qualifications.values('qualification'))
        departments = Department.objects.all()
        employees = User.objects.all()
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


def delete_shift(request, **kwargs):
    shift_id = kwargs['pk']
    selected_shift = Shift.objects.get(id=shift_id)
    selected_shift.delete()
    messages.success(request, "Shift successfully deleted.")
    return redirect('shifts')


def shift_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Shift.objects.all()
        for entry in all_entries:
            qualifications = ShiftQualifications.objects.filter(shift_id=entry.id).order_by(
                'qualification__name')
            entry.qualifications = qualifications

    context = {
        'all_entries': all_entries,
    }
    return render(request, 'shifts/shift_list.html', context)
