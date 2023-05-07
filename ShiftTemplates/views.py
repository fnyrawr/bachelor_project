from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Departments.models import Department
from Qualifications.models import Qualification
from .forms import ShiftTemplateForm
from .models import ShiftTemplate, ShiftTemplateQualifications


class ShiftTemplateCreationView(CreateView):
    model = ShiftTemplate
    form_class = ShiftTemplateForm
    template_name = 'shiftTemplates/create_shift_template.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            shift_template = form.save()
            messages.success(request, "Shift template successfully created.")
            return redirect('shift_templates')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def add_qualification(request, **kwargs):
    shift_template_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    if not ShiftTemplateQualifications.objects\
            .filter(shift_template_id=selected_shift_template, qualification=qualification_id).exists():
        ShiftTemplateQualifications.objects.create(shift_template=selected_shift_template,
                                                   qualification=selected_qualification)

    return redirect('edit_shift_template', pk=shift_template_id)


def remove_qualification(request, **kwargs):
    shift_template_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    entry = ShiftTemplateQualifications.objects.filter(shift_template=shift_template_id,
                                                       qualification=qualification_id)
    if entry is not None:
        entry.delete()

    return redirect('edit_shift_template', pk=shift_template_id)


def edit_shift_template(request, **kwargs):
    shift_template_id = kwargs['pk']
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)

    if request.method == "POST":
        form = ShiftTemplateForm(request.POST)
        data = form.data
        if data['note'] != '':
            note = data['note']
        else:
            note = ''
        ShiftTemplate.objects.filter(id=shift_template_id).update(
            name=data['name'],
            department=data['department'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            break_duration=data['break_duration'],
            note=note
        )
        messages.success(request, "Shift template has been successfully updated.")
        return redirect('shift_templates')
    # GET request
    else:
        associated_qualifications = ShiftTemplateQualifications.objects.filter(shift_template=selected_shift_template)
        non_associated_qualifications = Qualification.objects.all().exclude(
            id__in=associated_qualifications.values('qualification'))
        departments = Department.objects.all()
        form = ShiftTemplateForm()
        context = {
            'form': form,
            'selected_shift_template': selected_shift_template,
            'departments': departments,
            'non_associated_qualifications': non_associated_qualifications,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'shiftTemplates/edit_shift_template.html', context)


def delete_shift_template(request, **kwargs):
    shift_template_id = kwargs['pk']
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    selected_shift_template.delete()
    messages.success(request, "Shift template successfully deleted.")
    return redirect('shift_templates')


def shift_template_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = ShiftTemplate.objects.all()
        for entry in all_entries:
            qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id).order_by(
                'qualification__name')
            entry.qualifications = qualifications

    context = {
        'all_entries': all_entries,
    }
    return render(request, 'shiftTemplates/shift_template_list.html', context)
