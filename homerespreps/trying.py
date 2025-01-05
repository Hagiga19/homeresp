from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# Mock data for HOD's inventory
hod_inventory = {
    "Toilet Paper": 10,
    "Dish Soap": 2,
    "Trash Bags": 5,
    "Milk": 1
}

# Mock data for Anna's guest tracking
daily_guest_lists = {}

def get_today_guest_list():
    today = date.today().isoformat()
    if today not in daily_guest_lists:
        daily_guest_lists[today] = {
            "Yahel": 0,
            "Anna": 0,
            "HOD": 0,
            "Amit": 0,
            "Shahaf": 0
        }
    return daily_guest_lists[today]

# Mock data for Amit's responsibilities
food_supply = {
    "Rice": 5,
    "Pasta": 10,
    "Eggs": 12
}
cleaning_schedule = []

# Mock data for Shahaf's responsibilities
alcohol_inventory = {
    "Beer": 10,
    "Wine": 5,
    "Whiskey": 2
}
house_issues = []

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/hod', methods=['GET', 'POST'])
def hod_tasks():
    global hod_inventory
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        quantity = request.form.get('quantity', type=int, default=0)
        action = request.form.get('action')

        if action == 'add' and item_name:
            hod_inventory[item_name] = hod_inventory.get(item_name, 0) + quantity
        elif action == 'delete' and item_name in hod_inventory:
            del hod_inventory[item_name]

    return render_template('hod.html', inventory=hod_inventory)

@app.route('/anna', methods=['GET', 'POST'])
def anna_tasks():
    guest_list = get_today_guest_list()
    if request.method == 'POST':
        member_name = request.form.get('member_name')
        guests = request.form.get('guests', type=int, default=0)
        if member_name in guest_list:
            guest_list[member_name] = guests

    return render_template('anna.html', guest_list=guest_list)

@app.route('/amit', methods=['GET', 'POST'])
def amit_tasks():
    global food_supply, cleaning_schedule
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_food':
            item_name = request.form.get('item_name')
            quantity = request.form.get('quantity', type=int, default=0)
            if item_name:
                food_supply[item_name] = food_supply.get(item_name, 0) + quantity

        elif action == 'delete_food':
            item_name = request.form.get('item_name')
            if item_name in food_supply:
                del food_supply[item_name]

        elif action == 'add_cleaning':
            place = request.form.get('place')
            responsible = request.form.get('responsible')
            if place and responsible:
                cleaning_schedule.append({"place": place, "responsible": responsible})

        elif action == 'delete_cleaning':
            try:
                index = int(request.form.get('index', -1))
                if 0 <= index < len(cleaning_schedule):
                    cleaning_schedule.pop(index)
            except ValueError:
                pass  # Ignore invalid indexes

    enumerated_schedule = list(enumerate(cleaning_schedule))  # Ensure indices are correctly passed
    return render_template('amit.html', food_supply=food_supply, cleaning_schedule=enumerated_schedule)

@app.route('/shahaf', methods=['GET', 'POST'])
def shahaf_tasks():
    global alcohol_inventory, house_issues
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_alcohol':
            item_name = request.form.get('item_name')
            quantity = request.form.get('quantity', type=int, default=0)
            if item_name:
                alcohol_inventory[item_name] = alcohol_inventory.get(item_name, 0) + quantity

        elif action == 'delete_alcohol':
            item_name = request.form.get('item_name')
            if item_name in alcohol_inventory:
                del alcohol_inventory[item_name]

        elif action == 'add_issue':
            issue = request.form.get('issue')
            if issue:
                house_issues.append(issue)

        elif action == 'delete_issue':
            index = int(request.form.get('index', -1))
            if 0 <= index < len(house_issues):
                house_issues.pop(index)

    enumerated_issues = list(enumerate(house_issues))
    return render_template('shahaf.html', alcohol_inventory=alcohol_inventory, house_issues=enumerated_issues)

if __name__ == '__main__':
    app.run(debug=True)
