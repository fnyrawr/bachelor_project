from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Departments.models import Department, DepartmentQualifications
from Qualifications.models import Qualification
from .forms import ShiftTemplateForm, SearchForm
from .models import ShiftTemplate, ShiftTemplateQualifications


class ShiftTemplateCreationView(CreateView):
    model = ShiftTemplate
    form_class = ShiftTemplateForm
    template_name = 'shiftTemplates/fragments/create_shift_template.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            shift_template = form.save()
            # get department qualifications and add them to created shift template
            dep_qualifications = DepartmentQualifications.objects.filter(department=shift_template.department)
            for dq in dep_qualifications:
                sq = ShiftTemplateQualifications(shift_template=shift_template, qualification=dq.qualification)
                sq.save()
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
        non_associated_qualifications = Qualification.objects.all().exclude(id__in=associated_qualifications.values('qualification'))
        departments = Department.objects.all()
        form = ShiftTemplateForm()
        context = {
            'form': form,
            'selected_shift_template': selected_shift_template,
            'departments': departments,
            'non_associated_qualifications': non_associated_qualifications,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'shiftTemplates/fragments/edit_shift_template.html', context)


def delete_shift_template(request, **kwargs):
    shift_template_id = kwargs['pk']
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    user = request.user
    if user.role == 'A' or user.role == 'E':
        selected_shift_template.delete()
        messages.success(request, "Shift template successfully deleted.")
    return redirect('shift_templates')


def get_qualifications(request, **kwargs):
    shift_template_id = kwargs['pk']
    selected_shift_template = ShiftTemplate.objects.get(id=shift_template_id)
    associated_qualifications = ShiftTemplateQualifications.objects.filter(shift_template=selected_shift_template)
    non_associated_qualifications = Qualification.objects.all().exclude(id__in=associated_qualifications.values('qualification'))
    context = {
        'shift_template_id': shift_template_id,
        'associated_qualifications': associated_qualifications,
        'non_associated_qualifications': non_associated_qualifications
    }

    return HttpResponse(render(request, 'shiftTemplates/fragments/shift_template_qualifications.html', context))


def shift_template_list(request):
    if request.method == "POST":
        data = SearchForm(request.POST).data
        department = data['department']
        keyword = data['keyword']

        q_department = Q()
        q_keyword = Q()
        if department != '':
            q_department = Q(department__name__icontains=department)
        if keyword != '':
            q_name = Q(name__icontains=keyword)
            q_note = Q(note__icontains=keyword)
            q_keyword = Q(q_name | q_note)
        entries = ShiftTemplate.objects.filter(q_department & q_keyword).order_by('department__name')
    else:
        entries = ShiftTemplate.objects.all()
    for entry in entries:
        qualifications = ShiftTemplateQualifications.objects.filter(shift_template_id=entry.id).order_by('qualification__name')
        entry.qualifications = qualifications
    departments = Department.objects.all().order_by('name')

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'departments': departments
    }
    if request.method == "POST":
        return HttpResponse(render(request, 'shiftTemplates/fragments/shift_template_table.html', context))
    return HttpResponse(render(request, 'shiftTemplates/shift_template_list.html', context))
