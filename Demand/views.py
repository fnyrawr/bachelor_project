from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Demand.forms import DemandForm
from Demand.models import Demand


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
