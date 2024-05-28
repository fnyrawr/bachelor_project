import base64
from datetime import datetime, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from ShiftTemplates.models import ShiftTemplate, ShiftTemplateQualifications
from Shifts.models import Shift, ShiftQualifications
from utils.create_timeline import draw_timeline
from .forms import DayTemplateForm, PasteTemplateForm, SearchForm
from .models import DayTemplate, DayShiftTemplates


class DayTemplateCreationView(CreateView):
    model = DayTemplate
    form_class = DayTemplateForm
    template_name = 'dayTemplates/fragments/create_day_template.html'

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
        associated_shift_templates = DayShiftTemplates.objects.filter(day_template=selected_day_template)\
            .order_by('shift_template__start_time', 'shift_template__end_time', 'shift_template__name')
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
        # get timeline rendered
        shift_templates = []
        for template in associated_shift_templates:
            shift_templates.append(template.shift_template)
        timeline = None
        if len(shift_templates) > 0:
            contents = draw_timeline(shift_templates, 'day_templates')
            timeline = base64.b64encode(contents).decode()
        form = DayTemplateForm()
        context = {
            'form': form,
            'selected_day_template': selected_day_template,
            'non_associated_shift_templates': non_associated_shift_templates,
            'associated_shift_templates': associated_shift_templates,
            'timeline': timeline
        }
        return render(request, 'dayTemplates/fragments/edit_day_template.html', context)


def delete_day_template(request, **kwargs):
    day_template_id = kwargs['pk']
    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    user = request.user
    if user.role == 'A' or user.role == 'E':
        selected_day_template.delete()
        messages.success(request, "Day template successfully deleted.")
    return redirect('day_templates')


def paste_shifts_to_date(request, **kwargs):
    day_template_id = kwargs['pk']

    if request.method == "POST":
        form = PasteTemplateForm(request.POST)
        data = form.data
        shifts = DayShiftTemplates.objects.filter(day_template=day_template_id)
        to_date = data['to_date']

        for shift in shifts:
            start = to_date + ' ' + str(shift.shift_template.start_time)[:5]
            if shift.shift_template.start_time < shift.shift_template.end_time:
                end = to_date + ' ' + str(shift.shift_template.end_time)[:5]
            else:
                end = (datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)) \
                                  .strftime('%Y-%m-%d') + ' ' + str(shift.shift_template.end_time)[:5]
            start = datetime.strptime(start, "%Y-%m-%d %H:%M")
            end = datetime.strptime(end, "%Y-%m-%d %H:%M")
            qualifications = shift.shift_template.get_qualifications()

            new_shift = Shift(
                department=shift.shift_template.department,
                employee=None,
                start=start,
                end=end,
                break_duration=shift.shift_template.break_duration,
                note=shift.shift_template.note,
                highlight=False
            )
            new_shift.save()
            for qualification in qualifications:
                print(qualification.qualification)
                new_qualification = ShiftQualifications(
                    shift=new_shift,
                    qualification=qualification.qualification
                )
                new_qualification.save()
        messages.success(request, "Successfully pasted shifts.")

    return redirect('view_day_template', pk=day_template_id)


def view_day_template(request, **kwargs):
    day_template_id = kwargs['pk']
    selected_day_template = DayTemplate.objects.get(id=day_template_id)
    associated_shift_templates = DayShiftTemplates.objects.filter(day_template=selected_day_template)\
        .order_by('shift_template__start_time', 'shift_template__end_time', 'shift_template__name')
    for entry in associated_shift_templates:
        qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id) \
            .order_by('qualification__name')
        entry.qualifications = qualifications
    # get timeline rendered
    shift_templates = []
    for template in associated_shift_templates:
        shift_templates.append(template.shift_template)
    contents = draw_timeline(shift_templates, 'day_templates')
    timeline = base64.b64encode(contents).decode()
    context = {
        'selected_day_template': selected_day_template,
        'associated_shift_templates': associated_shift_templates,
        'timeline': timeline
    }
    return render(request, 'dayTemplates/fragments/day_template_detail.html', context)


def day_template_list(request):
    if request.method == "POST":
        data = SearchForm(request.POST).data
        keyword = data['keyword']

        q = Q()
        if keyword != '':
            q_name = Q(name__icontains=keyword)
            q_note = Q(description__icontains=keyword)
            q = Q(q_name | q_note)
        entries = DayTemplate.objects.filter(q).order_by('name')
    else:
        entries = DayTemplate.objects.all()
        for entry in entries:
            shift_templates = DayShiftTemplates.objects.filter(day_template_id=entry.id).order_by('shift_template__name')
            entry.shift_templates = shift_templates

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'entries': entries.count()
    }
    if request.method == 'POST':
        return HttpResponse(render(request, 'dayTemplates/fragments/day_template_table.html', context))
    return HttpResponse(render(request, 'dayTemplates/day_template_list.html', context))
