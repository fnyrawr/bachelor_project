import base64

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Demand.forms import DemandForm, SearchForm
from Demand.models import Demand
from Departments.models import Department
from utils.create_timeline import draw_timeline


class DemandCreationView(CreateView):
    model = Demand
    form_class = DemandForm
    template_name = 'demand/fragments/create_demand.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Demand successfully created.")
            return redirect('demand')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def edit_demand(request, **kwargs):
    demand_id = kwargs['pk']
    selected_demand = Demand.objects.get(id=demand_id)

    if request.method == "POST":
        form = DemandForm(request.POST)
        data = form.data
        if data['note'] != '':
            note = data['note']
        else:
            note = ''
        Demand.objects.filter(id=demand_id).update(
            department=data['department'],
            weekday=data['weekday'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            staff_count=data['staff_count'],
            note=note
        )
        messages.success(request, "Demand has been successfully updated.")
        return redirect('demand')
    # GET request
    else:
        departments = Department.objects.all()
        form = DemandForm()
        context = {
            'form': form,
            'selected_demand': selected_demand,
            'departments': departments
        }
        return render(request, 'demand/fragments/edit_demand.html', context)


def delete_demand(request, **kwargs):
    demand_id = kwargs['pk']
    selected_demand = Demand.objects.get(id=demand_id)
    user = request.user
    if user.role == 'A' or user.role == 'E':
        selected_demand.delete()
        messages.success(request, "Demand successfully deleted.")
    return redirect('demand')


def demand_list(request):
    if request.method == "POST":
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        weekday = data['weekday']
        department = data['department']
        q_weekday = Q()
        q_department = Q()
        if weekday != '0':
            q_weekday = Q(weekday=weekday)
        if department != '0':
            q_department = Q(department=department)
        if weekday != '0' or department != '0':
            q = Q(q_weekday & q_department)
            entries = Demand.objects.filter(q)
        else:
            entries = Demand.objects.all()

        # get timeline rendered
        if weekday != '0' and department != '0':
            contents = draw_timeline(entries, 'demand')
            timeline = base64.b64encode(contents).decode()
        else:
            timeline = None
    else:
        entries = Demand.objects.all()
        data = None
        timeline = None
    entries.order_by('department__name')
    departments = Department.objects.all()

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'form': SearchForm,
        'data': data,
        'departments': departments,
        'timeline': timeline,
        'range': range(24),
    }
    if request.method == 'POST':
        return HttpResponse(render(request, 'demand/fragments/demand_table.html', context))
    return HttpResponse(render(request, 'demand/demand_list.html', context))
