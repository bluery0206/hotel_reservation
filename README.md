# Student Scoring System

A Django-based web application for instructors to manage student scores and academic records offline.

## Features
### User Management
- Role-based views (User/Superuser)
- Profile editing (picture, name, email)
- Password change with old password verification
- Password recovery via email
- Account deletion
  
### Room Booking
- Date conflict prevention
- Upfront payment (no refunds)
- Check-in/check-out system
- Room name search functionality
- Fully responsive design

### Admin Features
- Amenities management (CRUD operations)
- Room management (add/delete/update)
- Reservation oversight
- Bulk delete operations
  
## Stack
- **Backend**: Python 3.12.3 (Django 5.2)
- **Frontend**: Halfmoon CSS
- **Database**: SQLite (Django's Default)
- **Authentication**: Django's built-in auth sytem

### Payment Integration
- Simulated payment processing
- No-refund policy enforcement

## Installation

1. Clone the repository:
``` bash
git clone https://github.com/bluery0206/room-reservation
```

2. Create virtual environment:
``` bash
python -m venv venv
```
   If it doesn't work, try replacing `python` with `py`, or `python3`.

3. Activate the virtual environment:
``` bash
# for Windows
venv\scripts\activate
```
``` bash
# for Linux
source venv/bin/activate
```

4. Install requirements:
``` bash
pip install -r requirements.txt
```

5. Initialize database:
``` bash
python3 manage.py makemigrations
python3 manage.py migrate
```

6. [OPTIONAL] Create superuser/admin:
``` bash
python3 manage.py createsuperuser
```  
   Then set your own admin account.

7. Run development server:
``` bash
python manage.py runserver
```

8. Open your sever by going to `localhost:8000/` in your browser.

## Usage

### Regular Users
- Browse available rooms
- View room details (click images to expand)
- Make reservations (payment required)
- Manage personal profile
- Check-in/check-out functionality

### Userusers
- Full CRUD for rooms and amenities
- Bulk delete operations
- Reservation management
- System oversight

## Business Logic
### Reservation Rules
- Payments are processed upfront
- No refunds for early checouts
- Date conflicts automatically prevented
- Rooms remain reserved until booked end date

### Occupancy Tracking
- `date_checkin` marks physical occupancy
- `date_checkout` releases physical space
