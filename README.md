# Bachelor Project Implementation
Implementation of a staff management software tool as part of my bachelor thesis

[[_TOC_]]

## How to start Project
Follow all steps by order:
- python -m venv .venv
- .venv\scripts\activate
- pip install django
- pip install Pillow
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## Author

| Name             | Student ID | E-Mail                                              |
|------------------|------------|-----------------------------------------------------|
| **Florian Kate** | 923081     | s51541@bht-berlin.de<br/>Florian.Kate.Bln@gmail.com |

### Status updates
    - `ToDo` not yet started
    - `WIP` currently work in progress
    - `OnHold` work in progress but currently no active development
    - `Testing` work is basically done, currently testing the features before migrating
    - `Done` done and pushed to repository

## General overview

- Django WebApp for a Staff management system
> Deadline for bachelor thesis: 2022-07-11

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
- (department, workhours, holiday_daycount in extra linked tables for history if changes happen)

### Qualifications
- name
- description
- is_important

> `Important` `Testing` `2023-04-26`

### Departments
- name
- description

> `Important` `WIP` `2023-04-26`

## Functions
### Needed
- [ ] Landing page
  - [ ] Infopage if not logged in
  - [ ] Admin dashboard [admin]
  - [ ] Planner dashboard [planner] (extending Employee dashboard)
  - [ ] Employee dashboard [employee]
- [ ] Departments
  - [ ] Create department [admin]
  - [ ] Manage department qualifications [admin]
  - [ ] Additional information [admin]
- [ ] Employees
  - [x] create employee user account [admin]
  - [x] Manage employee base data [admin]
  - [ ] Manage employee qualifications [admin]
  - [ ] Manage employee general availabilities [admin]
  - [ ] Manage employee shift wishes [admin]
- [ ] My account
  - [ ] Overview base data [all users]
  - [ ] Overview work hours [all users]
  - [ ] Overview availabilities [all users]
  - [x] Manage base data [all users]
  - [x] Change password [all users]
  - [ ] Recover password [all users]
  - [ ] Manage general availabilities [all users]
  - [ ] Manage shift wishes [all users]
