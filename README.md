# Bachelor Project Implementation
Implementation of a staff management software tool as part of my bachelor thesis

## How to start Project
Follow all steps by order:
- python -m venv .venv
- .venv\scripts\activate
- pip install django
- pip install Pillow
- pip install pandas
- pip install openpyxl
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

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
- ~~importers~~ [done]
- search and pagination [ToDo]
- shifts [ToDo]

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
  - [ ] Restricted access note
  - [x] Reset password
  - [ ] Admin dashboard [admin]
  - [ ] Planner dashboard [planner] (extending Employee dashboard)
  - [ ] Employee dashboard [employee]
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
  - [x] Manage employee holidays [admin]
- [ ] Shifts
  - [x] Manage demand [admin]
  - [x] Manage Shift templates [admin]
  - [x] Manage Day templates [admin]
  - [ ] Timeline view
  - [x] Create shifts for dates
  - [ ] Copy day templates to dates
  - [ ] Cloning weeks
  - [ ] Assign employees
    - [ ] Assign helper with AI tools / rule based
- [ ] My account
  - [x] Overview base data [all users]
  - [ ] Overview work hours [all users]
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
  - [ ] Exporting data
