from datetime import datetime, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from Users.models import User
from .models import Wish
from .forms import WishForm, SearchForm


class WishCreationView(CreateView):
    model = Wish
    form_class = WishForm
    template_name = 'wishes/fragments/create_wish.html'

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
    template_name = 'attendance/fragments/add_own_wish.html'

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
        return render(request, 'wishes/fragments/edit_wish.html', context)


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
        return HttpResponse(render(request, 'attendance/fragments/edit_own_wish.html', context))


def delete_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)
    user = request.user
    if user.role == 'A':
        selected_wish.delete()
        messages.success(request, "Wish successfully deleted.")
    return redirect('wishes')


def delete_own_wish(request, **kwargs):
    wish_id = kwargs['pk']
    selected_wish = Wish.objects.get(id=wish_id)
    user = request.user
    if selected_wish.employee == user:
        selected_wish.delete()
        messages.success(request, "Wish successfully deleted.")
    return redirect('own_wishes')


def own_wishes(request):
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        keyword = data['keyword']
        q_date = Q()
        q_keyword = Q()

        q_user = Q(employee=request.user)
        if filter_date is not None and filter_date != '':
            # filter week around date
            filter_date = datetime.strptime(filter_date, '%Y-%m-%d')
            date_min = filter_date - timedelta(days=filter_date.weekday())
            date_max = filter_date + timedelta(days=6-filter_date.weekday())
            q_date_min = Q(date__gte=date_min)
            q_date_max = Q(date__lte=date_max)
            q_date = Q(q_date_min & q_date_max)
        if keyword is not None and keyword != '':
            q_keyword = Q(note__icontains=keyword)
        q = Q(q_user & Q(q_date & q_keyword))
        entries = Wish.objects.filter(q)
    else:
        # filter last week and future
        filter_date = datetime.today().strftime('%Y-%m-%d')
        date_min = datetime.today()-timedelta(days=datetime.today().weekday()+7)
        searchForm = SearchForm()
        data = searchForm.data
        data['filter_date'] = filter_date
        q_user = Q(employee=request.user)
        q_date = Q(date__gte=date_min)
        q = Q(q_user & q_date)
        entries = Wish.objects.filter(q).order_by('date')
        if entries.count() == 0:
            return HttpResponse('<h6><i class="material-icons accent-color-text left">info</i>No shift wishes set for last week and in the future</h6>')

    context = {
        'all_entries': entries,
        'form': SearchForm,
        'search': search,
        'data': data
    }
    if entries.count() == 0:
        return HttpResponse('<h6><i class="material-icons accent-color-text left">info</i>No shift wishes matching your filters</h6>')
    return HttpResponse(render(request, 'attendance/fragments/own_wishes.html', context))


def wish_list(request):
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        filter_date = data['filter_date']
        filter_is_available = data['filter_is_available']
        filter_tendency = data['filter_tendency']
        keyword = data['keyword']
        q_date = Q()
        q_is_available = Q()
        q_tendency = Q()
        q_keyword = Q()

        if filter_date != '':
            q_date = Q(date__exact=filter_date)
        if int(filter_is_available) == 0:
            q_is_available = Q(is_available__exact=False)
        if int(filter_is_available) == 1:
            q_is_available = Q(is_available__exact=True)
        if int(filter_tendency) > -1:
            q_tendency = Q(tendency__exact=filter_tendency)
        if keyword != '':
            last_name = Q(employee__last_name__icontains=keyword)
            first_name = Q(employee__first_name__icontains=keyword)
            note = Q(note__icontains=keyword)
            q_keyword = Q(last_name | first_name | note)
        q = Q(q_date & q_is_available & q_tendency & q_keyword)
        entries = Wish.objects.filter(q)
    else:
        filter_date = datetime.today().strftime('%Y-%m-%d')
        searchForm = SearchForm()
        data = searchForm.data
        data['filter_date'] = filter_date
        q_date = Q(date__exact=filter_date)
        entries = Wish.objects.filter(q_date)

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
    if request.method == 'POST':
        return HttpResponse(render(request, 'wishes/fragments/wish_table.html', context))
    return HttpResponse(render(request, 'wishes/wish_list.html', context))
