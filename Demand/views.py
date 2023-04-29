from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Demand.forms import DemandForm
from Demand.models import Demand
from Departments.models import Department


class DemandCreationView(CreateView):
    model = Demand
    form_class = DemandForm
    template_name = 'demand/create_demand.html'

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
        return render(request, 'demand/edit_demand.html', context)


def delete_demand(request, **kwargs):
    demand_id = kwargs['pk']
    selected_demand = Demand.objects.get(id=demand_id)
    selected_demand.delete()
    messages.success(request, "Demand successfully deleted.")
    return redirect('demand')


def demand_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Demand.objects.order_by('department__name')

    context = {
        'all_entries': all_entries,
    }
    return render(request, 'demand/demand_list.html', context)
