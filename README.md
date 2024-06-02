# ShiftManager
This project was part of my Bachelor Thesis. It is currently `June 2024` under rework for better user experience and some major overhaul.

### How to make the application run
1) create a virtual environment
> python -m venv .venv  
> .venv\scripts\activate (Windows)  
> .venv/script/activate (Linux/Mac/Unix)
2) install requirements (dependencies)
> pip install -r requirements.txt
3) generate a secret key (length=30, full charset)
4) create secret_key.py file in Settings folder and insert
> key = '`generated secret key`'
5prepare database
> python manage.py makemigrations  
> python manage.py migrate
6) create a superuser for administration
> python manage.py createsuperuser

`name, mail and password are required`

7) name the superuser and grant admin rights
> python manage.py shell  
> from Users.models import User  
> user = User.objects.get(username='`superuser_name`')  
> user.first_name = '`admin_first_name`'  
> user.last_name = '`admin_last_name`'  
> user.role = 'A'  
> user.save()

`close the shell with CTRL+Z + return`

8) run the server
> python manage.py runserver

9) login, then import or create data

## Author
| Name           | Github  |
|----------------|---------|
| **Florian K.** | fnyrawr |

### Status updates
    - `ToDo` not yet started
    - `WIP` currently work in progress
    - `OnHold` work in progress but currently no active development
    - `Testing` work is basically done, currently testing the features before migrating
    - `Done` done and pushed to repository

## General overview

- WebApp for a Staff management system
- Using Django (based on Python)
- Using HTMX for dynamic requests and MaterializeWeb for styling

## Current development
### UI
- [x] Reworking page design `Done` `2024-06-03`

### Functionality
- [ ] Implement change history `ToDo`
  - [ ] Name (first, last)
  - [ ] Contact data (address, telephone)
  - [ ] Contract data (start, end, external, active)
  - [ ] Department
  - [ ] Work hours
  - [ ] Holiday (yearly holiday allowance)
  - [x] User Qualifications
  - [ ] Salary
  - [ ] Surcharges
- [ ] Salary and Surcharges (not yet implemented) `ToDo`
- [ ] Demand integration `ToDo`
  - [ ] Generate shifts with AI depending on demand
- [ ] Shift assignment improvements `ToDo`
  - [ ] Better candidate suggestions
  - [ ] AI assisted assignments

### REST-API
- [ ] Users/Employees `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Qualifications `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Departments `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Demand `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Absences `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Holidays `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Availabilities `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Wishes `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Shift Templates `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Day Templates `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] Shifts `ToDo`
  - [ ] Import
  - [ ] Export
  - [ ] Testing
- [ ] automatic test data creation script `ToDo`

### Bugfixes
- [ ] CSS fixes (Input showing wrong label color on focus) `ToDo`
- [ ] User/Employee edit: redirect to respective page `ToDo`
- [ ] Holiday/Absence filters to be more intuitive `ToDo`
  - [ ] Absence: don't change filters after creating/changing absence `ToDo`
  - [ ] Holiday: don't change filters after creating/changing holiday `ToDo`
- [ ] Shifts filters to be more intuitive `ToDo`
  - [ ] Don't change filters after creating/changing shifts `ToDo`
