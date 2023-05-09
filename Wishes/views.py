from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Wish
from .forms import WishForm, SearchForm


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
    data = None
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        filter_tendency = data['filter_tendency']
        keyword = data['keyword']
        q_date = Q()
        q_tendency = Q()
        q_keyword = Q()

        if filter_date != '':
            q_date = Q(date__exact=filter_date)
        if int(filter_tendency) > -1:
            q_tendency = Q(tendency__exact=filter_tendency)
        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | note)
        q = Q(q_date & q_tendency & q_keyword)
        entries = Wish.objects.filter(q)
    else:
        entries = Wish.objects.all()

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data
    }
    return render(request, 'wishes/wish_list.html', context)
