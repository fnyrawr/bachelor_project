from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Wish
from .forms import WishForm


class WishCreationView(CreateView):
    model = Wish
    form_class = WishForm
    template_name = 'wishes/create_wish.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # delete entry if exists and create new
            wish = Wish.objects.filter(employee=request.POST['employee'],
                                       date=request.POST['date'])
            if wish is not None:
                wish.delete()
            wish = form.save()
            messages.success(request, "Wish successfully created.")
            return redirect('wishes')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


class OwnWishCreationView(CreateView):
    model = Wish
    form_class = WishForm
    template_name = 'wishes/add_own_wish.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # delete entry if exists and create new
            wish = Wish.objects.filter(employee=request.user,
                                       date=request.POST['date'])
            if wish is not None:
                wish.delete()
            wish = form.save()
            messages.success(request, "Wish successfully created.")
            return redirect('own_wishes')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {'form': form})


def edit_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)

    if request.method == "POST":
        form = WishForm(request.POST)
        data = form.data
        if 'is_available' in data:
            is_available = True
        else:
            is_available = False
        if data['start_time'] == '':
            start_time = None
        else:
            start_time = data['start_time']
        if data['end_time'] == '':
            end_time = None
        else:
            end_time = data['end_time']
        Wish.objects.filter(id=wish_id).update(
            employee=data['employee'],
            date=data['date'],
            is_available=is_available,
            start_time=start_time,
            end_time=end_time,
            tendency=data['tendency'],
            note=data['note']
        )
        messages.success(request, "Wish has been successfully updated.")
        return redirect('wishes')
    # GET request
    else:
        employees = User.objects.all()
        form = WishForm()
        context = {
            'form': form,
            'selected_wish': selected_wish,
            'employees': employees
        }
        return render(request, 'wishes/edit_wish.html', context)


def edit_own_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)

    if request.method == "POST":
        form = WishForm(request.POST)
        data = form.data
        if 'is_available' in data:
            is_available = True
        else:
            is_available = False
        if data['start_time'] == '':
            start_time = None
        else:
            start_time = data['start_time']
        if data['end_time'] == '':
            end_time = None
        else:
            end_time = data['end_time']
        Wish.objects.filter(id=wish_id).update(
            employee=data['employee'],
            date=data['date'],
            is_available=is_available,
            start_time=start_time,
            end_time=end_time,
            tendency=data['tendency'],
            note=data['note']
        )
        messages.success(request, "Wish has been successfully updated.")
        return redirect('own_wishes')
    # GET request
    else:
        form = WishForm()
        context = {
            'form': form,
            'selected_wish': selected_wish
        }
        return render(request, 'wishes/edit_own_wish.html', context)


def delete_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)
    selected_wish.delete()
    messages.success(request, "Wish successfully deleted.")
    return redirect('wishes')


def delete_own_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)
    selected_wish.delete()
    messages.success(request, "Wish successfully deleted.")
    return redirect('own_wishes')


def own_wishes(request):
    user = request.user
    all_entries = None
    all_entries = Wish.objects.filter(employee=user).order_by('date')

    context = {
        'all_entries': all_entries
    }
    return render(request, 'wishes/own_wishes.html', context)


def wish_list(request):
    all_entries = None
    entries_found = None
    search = False

    if request.method == "POST":
        search = True
    else:
        all_entries = Wish.objects.all()

    context = {
        'all_entries': all_entries
    }
    return render(request, 'wishes/wish_list.html', context)
