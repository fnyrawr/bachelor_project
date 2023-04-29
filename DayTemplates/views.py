from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from ShiftTemplates.models import ShiftTemplate, ShiftTemplateQualifications
from .forms import DayTemplateForm
from .models import DayTemplate, DayShiftTemplates


class DayTemplateCreationView(CreateView):
    model = DayTemplate
    form_class = DayTemplateForm
    template_name = 'dayTemplates/create_day_template.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            day_template = form.save()
            messages.success(request, "Day template successfully created.")
            return redirect('day_templates')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def add_shift_template(request, **kwargs):
    day_template_id = kwargs['pk1']
    shift_template_id = kwargs['pk2']

    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    if not DayShiftTemplates.objects\
            .filter(day_template=selected_day_template, shift_template=selected_shift_template).exists():
        DayShiftTemplates.objects.create(day_template=selected_day_template, shift_template=selected_shift_template)

    return redirect('edit_day_template', pk=day_template_id)


def remove_shift_template(request, **kwargs):
    day_template_id = kwargs['pk1']
    shift_template_id = kwargs['pk2']

    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    entry = DayShiftTemplates.objects.filter(day_template=selected_day_template, shift_template=selected_shift_template)
    if entry is not None:
        entry.delete()

    return redirect('edit_day_template', pk=day_template_id)


def edit_day_template(request, **kwargs):
    day_template_id = kwargs['pk']
    selected_day_template = DayTemplate.objects.get(id=day_template_id)

    if request.method == "POST":
        form = DayTemplateForm(request.POST)
        data = form.data
        if data['description'] != '':
            description = data['description']
        else:
            description = ''
        DayTemplate.objects.filter(id=day_template_id).update(
            name=data['name'],
            description=description
        )
        messages.success(request, "Day template has been successfully updated.")
        return redirect('day_templates')
    # GET request
    else:
        associated_shift_templates = DayShiftTemplates.objects.filter(day_template=selected_day_template)
        for entry in associated_shift_templates:
            qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id)\
                .order_by('qualification__name')
            entry.qualifications = qualifications
        non_associated_shift_templates = ShiftTemplate.objects.all().exclude(
            id__in=associated_shift_templates.values('shift_template'))
        for entry in non_associated_shift_templates:
            qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id).order_by(
                'qualification__name')
            entry.qualifications = qualifications
        form = DayTemplateForm()
        context = {
            'form': form,
            'selected_day_template': selected_day_template,
            'non_associated_shift_templates': non_associated_shift_templates,
            'associated_shift_templates': associated_shift_templates
        }
        return render(request, 'dayTemplates/edit_day_template.html', context)


def delete_day_template(request, **kwargs):
    day_template_id = kwargs['pk']
    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    selected_day_template.delete()
    messages.success(request, "Day template successfully deleted.")
    return redirect('day_templates')


def view_day_template(request, **kwargs):
    day_template_id = kwargs['pk']
    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    associated_shift_templates = DayShiftTemplates.objects.filter(day_template=selected_day_template)
    for entry in associated_shift_templates:
        qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id) \
            .order_by('qualification__name')
        entry.qualifications = qualifications
    context = {
        'selected_day_template': selected_day_template,
        'associated_shift_templates': associated_shift_templates
    }
    return render(request, 'dayTemplates/day_template_detail.html', context)


def day_template_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = DayTemplate.objects.all()
        for entry in all_entries:
            shift_templates = DayShiftTemplates.objects.filter(day_template_id=entry.id).order_by(
                'shift_template__name')
            entry.shift_templates = shift_templates

    context = {
        'all_entries': all_entries,
    }
    return render(request, 'dayTemplates/day_template_list.html', context)
