# Bachelor Project Implementation
Implementation of a staff management software tool as part of my bachelor thesis

### How to make the application run
1) create a virtual environment
> python -m venv .venv  
> .venv\scripts\activate
2) install requirements (dependencies)
> pip install -r requirements.txt
3) prepare database
> python manage.py makemigrations  
> python manage.py migrate
4) create a superuser for administration
> python manage.py createsuperuser

`name, mail and password are required`

5) name the superuser and grant admin rights
> python manage.py shell  
> from Users.models import User  
> user = User.objects.get(username='`superuser_name`')  
> user.first_name = '`admin_first_name`'  
> user.last_name = '`admin_last_name`'  
> user.role = 'A'  
> user.save()

`close the shell with CTRL+Z + return`

6) run the server
> python manage.py runserver

7) login, then import or create data

## Author
| Name           | Github  | E-Mail               |
|----------------|---------|----------------------|
| **Florian K.** | fnyrawr | s51541@bht-berlin.de |

### Status updates
    - `ToDo` not yet started
    - `WIP` currently work in progress
    - `OnHold` work in progress but currently no active development
    - `Testing` work is basically done, currently testing the features before migrating
    - `Done` done and pushed to repository

## General overview

- Django WebApp for a Staff management system
> Deadline for bachelor thesis: 2022-07-11

### upcoming next ToDos
- landing page [toDo]
- dashboard (Admin/Planner/~~Employee~~) [WIP]
- ~~export shiftplan as PDF file~~ [done]
- employee assign helper [toDo]
- data export [toDo]

## Database
### Employee
- username
- email
- password
- lastname
- firstname
- staff_id
- role
- external
- telephone_home
- telephone_mobile
- address
- zip_city
- active
- verified
- last_login
- start_contract
- end_contract
- department
- work_hours
- holiday_count

> `Important` `Done` `2023-04-25`

### Qualifications
- name
- description
- is_important

> `Important` `Done` `2023-04-26`

### Departments
- name
- description

> `Important` `Done` `2023-04-26`

### EmployeesQualifications
- employee_id
- qualification_id

> `Important` `Done` `2023-04-27`

### DepartmentsQualifications
- department_id
- qualification_id

> `Important` `Done` `2023-04-27`

### Demand
- demand_id
- weekday
- start_time
- end_time
- staff_count
- note

> `Optional` `Done` `2023-04-28`

### ShiftTemplates
- shift_template_id
- name
- department
- start_time
- end_time
- break_duration
- note

> `Important` `Done` `2023-04-29`

### ShiftTemplatesQualifications
- shift_template_id
- qualification_id

> `Important` `Done` `2023-04-29`

### DayTemplates
- day_template_id
- name
- description

> `Important` `Done` `2023-04-29`

### DayShiftTemplates
- day_template_id
- shift_template_id

> `Important` `Done` `2023-04-29`

### Availabilities
- employee
- weekday
- start_time
- end_time
- tendency
- is_available
- note

> `Important` `Done` `2023-05-02`

### Wishes
- employee
- date
- start_time
- end_time
- tendency
- is_available
- note

> `Important` `Done` `2023-05-02`

### Absences
- employee
- start_date
- end_date
- absence_type
- status
- note

> `Important` `Done` `2023-05-03`

### Holidays
- employee
- start_date
- end_date
- status
- note

> `Important` `Done` `2023-05-03`

### Shifts
- shift_id
- department
- employee
- start
- end
- break_duration
- note
- highlight

> `Important` `Done` `2023-05-07`

## Functions
### Needed
- [ ] Landing page
  - [ ] Infopage if not logged in
  - [x] Restricted access note
  - [x] Reset password
  - [ ] Admin dashboard [admin]
  - [ ] Planner dashboard [planner] (extending Employee dashboard)
  - [x] Employee dashboard [employee]
- [x] Departments
  - [x] Create department [admin]
  - [x] Manage department qualifications [admin]
  - [x] Additional information [admin]
- [x] Employees
  - [x] create employee user account [admin]
  - [x] Manage employee base data [admin]
  - [x] Manage employee qualifications [admin]
  - [x] Manage employee general availabilities [admin]
  - [x] Manage employee shift wishes [admin]
  - [x] Manage employee absences [admin]
    - [x] unmatch employee from shifts in timeframe on approve
  - [x] Manage employee holidays [admin]
    - [x] unmatch employee from shifts in timeframe on approve
- [ ] Shifts
  - [x] Manage demand [admin]
  - [x] Manage Shift templates [admin]
  - [x] Manage Day templates [admin]
  - [x] Timeline view
  - [x] Create shifts for dates
  - [x] Copy day templates to dates
  - [ ] Cloning weeks
  - [x] Assign employees
    - [x] Filter out already assigned that day
    - [x] Filter out absent/holiday
    - [ ] Assign helper rule based
  - [x] shift plan displayed on page
  - [x] create shift plan as PDF
- [x] My account
  - [x] Overview base data [all users]
  - [x] Overview work hours [all users]
  - [x] Overview absences and holiday [all users]
  - [x] Manage base data [all users]
  - [x] Change password [all users]
  - [x] Manage general availabilities [all users]
  - [x] Manage shift wishes [all users]
- [ ] Data management
  - [x] Importer for Qualifications
  - [x] Importer for Departments
  - [x] Importer for Users
  - [x] Importer for Absence
  - [x] Importer for Holiday
  - [x] Importer for Demand
  - [x] Importer for ShiftTemplates
  - [x] Importer for DayTemplates
  - [x] Importer for General availabilities
  - [x] Importer for Shift wishes
  - [x] Importer for Shifts
  - [ ] Exporting data `WIP`
