import json
import calendar
from datetime import datetime, timedelta
import itertools

current_date = datetime.today().strftime("%Y-%m-%d")
current_year = int(datetime.today().strftime("%Y"))
current_month = int(datetime.today().strftime("%m"))
current_day = int(datetime.today().strftime("%d"))

def start_screen(user_name, user_choice):
    if user_choice == "Create":
        print("Perfect! Now I will ask you some questions, to create two files with all your data")
        print("One of the files, named {}.json, will collect all your starting data".format(user_name))
        print("The other one, named {}_records.json, will collect all your records about dates cycled and expenses,\ntracking a balance between your saves and your expenses".format(user_name))
        print("You can find both files in the same folder of this program. Let's start!")
        create_json_data(user_name)
        create_json_records(user_name)
    if user_choice == "Update":
        user_update_expenses = input("Would you like to update your data or add any expenses?(Data/Expenses): ")
        if user_update_expenses == "Data":
            update_dates_cycled(user_name)
        if user_update_expenses == "Expenses":
            expenses_reason = input("What did you buy?: ")
            expenses_price = float(input("How much did it cost?: "))
            expenses_date = input("When did you buy it(yyyy-mm-dd)?: ")
            year, month, day = map(str, expenses_date.split('-'))
            update_dates_expended(expenses_reason, expenses_price, user_name, day, month, year)
    if user_choice == "Keep name":
        user_update_expenses = input("Would you like to update your data or add any expenses?(Data/Expenses): ")
        if user_update_expenses == "Data":
            update_dates_cycled(user_name)
        if user_update_expenses == "Expenses":
            expenses_reason = input("What did you buy?: ")
            expenses_price = float(input("How much did it cost?: "))
            expenses_date = input("When did you buy it(yyyy-mm-dd)?: ")
            year, month, day = map(str, expenses_date.split('-'))
            update_dates_expended(expenses_reason, expenses_price, user_name, day, month, year)
    if user_choice == "New name":
        try:
            data = open("{}.json".format(user_name))
            data.close()
            records = open("{}_records.json".format(user_name))
            records.close()
            print("Hello again {}, your options are:\n - Update your database(Update)\n - Exit the program(Exit)\n")
            user_choice = input("What would you like to do?: ")
            if user_choice == "Update":
                start_screen(user_name, user_choice)
            if user_choice == "Exit":
                start_screen(user_name, user_choice)
        except FileNotFoundError:
            print("Hello {}, your options are:\n - Create a new database(Create)\n - Exit the program(Exit)\n".format(user_name))
            user_choice = input("What would you like to do?: ")
            if user_choice == "Create":
                start_screen(user_name, user_choice)
            if user_choice == "Exit":
                start_screen(user_name, user_choice)
    if user_choice == "Exit":
        print("See you next time, thanks {}!".format(user_name))
        exit()

def create_json_data(user_name):
#Questions
    start_year = int(input("Which year did you start to commute by bike: "))
    start_month = int(input("Which month (number)?: "))
    start_day = int(input("Which day?: "))
    list_years_cycling = list(range(start_year, current_year + 1))
    bike_price = float(input("How much does your bike cost?: "))
    price_go = float(input("How much does your way to work usually cost?: "))
    price_return = float(input("How much does your way back to home usually cost?: "))
#Create the Data document
    with open("{}.json".format(user_name), "w") as f:
        json.dump({"Years":[],"Starting date":[],"Price of the bike": 0,"Price per commute":[]}, f, indent=4)
#Get the years as a list of nested lists, where each of it represents a month with the list of days inside
    for y in list_years_cycling:
        months_as_list = []
        for m in range(1, 13):
            month = calendar.monthcalendar(y, m)
            flat_list = []
            for sublist in month:
                for item in sublist:
                    flat_list.append(item)              
            no_zero_list = []
            for e in flat_list:
                if e != 00:
                    no_zero_list.append("%02d" % e)
            months_as_list.append(no_zero_list)
#Write the years on the file
        with open("{}.json".format(user_name), "r") as f:    
            dictionary = json.load(f)
        if type(dictionary["Years"]) == list:
            with open("{}.json".format(user_name), "r") as f:
                dictionary["Years"].append({y:months_as_list})
            with open("{}.json".format(user_name), "w") as f:
                json.dump(dictionary, f, indent=4)
#Write the starting date on the file
    if type(dictionary["Starting date"]) == list:
        with open("{}.json".format(user_name), "r") as f:
            dictionary["Starting date"].append({"Starting day":start_day})
            dictionary["Starting date"].append({"Starting month":start_month})
            dictionary["Starting date"].append({"Starting year":start_year})
        with open("{}.json".format(user_name), "w") as f:
            json.dump(dictionary, f, indent=4)
#Write the price of the bike on the file
    with open("{}.json".format(user_name), "r") as f:
        dictionary["Price of the bike"] = bike_price
    with open("{}.json".format(user_name), "w") as f:
        json.dump(dictionary, f, indent=4)
#Write the commute prices on the file
    if type(dictionary["Price per commute"]) == list:
        with open("{}.json".format(user_name), "r") as f:
            dictionary["Price per commute"].append({"Price to go":price_go})
            dictionary["Price per commute"].append({"Price to return":price_return})
        with open("{}.json".format(user_name), "w") as f:
            json.dump(dictionary, f, indent=4)
    
def create_json_records(user_name):    
#Extract data needed from the Data json file
    with open("{}.json".format(user_name), "r") as f:
        dictionary = json.load(f)
    for key, value in dictionary.items():
#Bike price
        if key == "Price of the bike":
            bike_price = value
#Starting dates
        if key == "Starting date":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == "Starting day":
                        start_day = value1
                    if key1 == "Starting month":
                        start_month = value1
                    if key1 == "Starting year":
                        start_year = value1
#Prices per commute
        if key == "Price per commute":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == "Price to go":
                        price_go = value1
                    if key1 == "Price to return":
                        price_return = value1       
#Create the recorded data .json document
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump({"Dates":[],"Total days cycled": 0,"Total saved": 0,"Expenses": [],"Total spent": 0,"Balance": -bike_price}, f, indent=4)
#Add first day data
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
#Date and save
        if type(records_dictionary["Dates"]) == list:
            with open("{}_records.json".format(user_name), "r") as f:    
                records_dictionary["Dates"].append({"{}".format(start_year):[{"{}".format('{:02d}'.format(start_month)):{"{}".format(start_day):price_go+price_return, "Total days cycled": 1, "Total saved": price_go+price_return}}]})
            with open("{}_records.json".format(user_name), "w") as f:
                json.dump(records_dictionary, f, indent=4)
#To Total and Balance
        for key, value in records_dictionary.items():
            if key == "Balance":
                Balance = value
        records_dictionary["Total saved"] = +price_go+price_return
        records_dictionary["Balance"] = Balance + (price_go+price_return)
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Call update dates cycled or start screen
    print("Your data have been created, you can find it in the same folder of this program")
    user_choice = input("Now, would you like to keep updating your data or go back to the start screen(Update/Back)?: ")
    if user_choice == "Update":
        print("Perfect! Now I will be iterating through the days since you start to cycle, until the current day")
        print("I will ask you for each day, and you have to answer with a 'Yes' or a 'No'")
        print("You can answer with a 'Not yet' if you still have no cycle on the current day")
        print("You can tell the program to 'Stop' the iteration, so you can retake it whenever you like since the last date you have been asked for")
        update_dates_cycled(user_name)
    if user_choice == "Back":
        user_choice_1 = input("{}, would you like to keep working on your name, work under any other name or exit the program (Keep name/New name/Exit)?: ".format(user_name))
        keepname_newname_exit(user_name, user_choice_1)

def update_dates_cycled(user_name):
#Read the documents
    with open("{}.json".format(user_name), "r") as f:
        dictionary = json.load(f)
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
#Get the last recorded day, month and year
    years_list = []
    months_list = []
    days_list = []
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    years_list.append(key1)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                months_list.append(key2)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key2 == months_list[-1]:
                                    for e2 in value2:
                                        if e2 != "Total days cycled" and e2 != "Total saved":
                                            days_list.append(e2)
    last_recorded_year = int(years_list[-1])
    last_recorded_month = int(months_list[-1])
    last_recorded_day = int(days_list[-1])
#Get price to go and price to return
    for key, value in dictionary.items():
        if key == "Price per commute":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == "Price to go":
                        price_go = value1
                    if key1 == "Price to return":
                        price_return = value1
#Iterate between the days asking if the user cycle or not when the last recorded date belongs to a different year than the current date
    if last_recorded_year != current_year:
        list_dimensioned = []
        months_between_lastrec_dec = []
        months_between_jan_current = []
        months_as_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        years_in_data_doc = []
        for e in months_as_list[last_recorded_month-1:]:
            months_between_lastrec_dec.append(e)
        for e in months_as_list[:current_month]:
            months_between_jan_current.append(e)
        for key, value in dictionary.items():    
            if key == "Years":
                for e in value:
                    for key1, value1 in e.items():
    #Iterate between the last date recorded and last day of the year
                        for m in months_between_lastrec_dec:
                            if key1 == str(last_recorded_year):
        #If month iterated is the same as the last recorded month but not the same as the current month
                                if m == last_recorded_month:
                                    for e in value1[m-1][last_recorded_day:]: 
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, last_recorded_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            print("Good")
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)                                            
        #If month iterated is neither the last recorded month nor the current month  
                                if m != last_recorded_month and m != current_month:
                                    for e in value1[m-1][:]:
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, last_recorded_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            print("Good")
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)                                    
    #Iterate between the first day of the year and the current date                        
                        for m in months_between_jan_current:
                            if key1 == str(current_year):
        #If month iterated is neither the last recorded month nor the current month  
                                if m != last_recorded_month and m != current_month:
                                    for e in value1[m-1][:]:
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            print("Good")
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)                                                    
        #If month iterated is the same as the current month, but the last recorded month is the past month 
                                if m == current_month and last_recorded_month != current_month:
                                    for e in value1[current_month-1][:current_day]:
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)         
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            if int(e) == current_day and m == current_month:
                                                if m <= 9:
                                                    dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                                else:
                                                    dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                                add_new_year(user_name, m)
                                                print("Good")
                                            else:
                                                print("Good")
            #Check if date before is on the list of dates cycled, if not add it with value 0
                                        if daily_check == "Not yet":
                                            not_yet(current_year, current_month, current_day, user_name)
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)
            #Return to start screen
                                    user_choice_1 = input("{}, your records are up to date, would you like to keep working on your name, work under any other name or exit the program (Keep name/New name/Exit)?: ".format(user_name))
                                    keepname_newname_exit(user_name, user_choice_1)    
#Iterate between the days asking if the user cycle or not when the last recorded date belongs to the same year as the current date 
    if last_recorded_year == current_year:
        list_dimensioned = []
        months_between_lastrec_current = list(range(last_recorded_month,current_month+1))
        for key, value in dictionary.items():    
            if key == "Years":
                for e in value:
                    for key1, value1 in e.items():
                        if key1 == str(current_year):
                            for m in months_between_lastrec_current: 
    #If month iterated is the same as the last recorded month and the current month 
                                if m == last_recorded_month and m == current_month:
                                    for e in value1[m-1][last_recorded_day:current_day]: 
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            if m > 9:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)    
                                        if daily_check == 'No':
                                            if int(e) == current_day and m == current_month:
                                                if m <= 9:
                                                    dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                                else:
                                                    dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                                add_new_year(user_name, m)
                                                print("Good")
                                            else:
                                                print("Good")
            #Check if date before is on the list of dates cycled, if not add it with value 0
                                        if daily_check == "Not yet":
                                            not_yet(current_year, current_month, current_day, user_name)
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)
            #Return to start screen
                                    user_choice_1 = input("{}, your records are up to date, would you like to keep working on your name, work under any other name or exit the program (Keep name/New name/Exit)?: ".format(user_name))
                                    keepname_newname_exit(user_name, user_choice_1)
    #If month iterated is the same as the last recorded month but not the same as the current month
                                if m == last_recorded_month and m != current_month:
                                    for e in value1[m-1][last_recorded_day:]: 
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            print("Good")
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)                                            
    #If month iterated is neither the last recorded month nor the current month  
                                if m != last_recorded_month and m != current_month:
                                    for e in value1[m-1][:]:
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            print("Good")
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)
    #If month iterated is the same as the current month, but the last recorded month is the past month 
                                if m == current_month and last_recorded_month != current_month:
                                    for e in value1[current_month-1][:current_day]:
                                        daily_check = input("Did you cycle on {}/{}/{}?: ".format(e, m, current_year))
                                        if daily_check == 'Yes':
                                            if m <= 9:
                                                dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                            else:
                                                dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                            add_new_year(user_name, m)
                                            last_date_empty_deleter(user_name)
                                        if daily_check == 'No':
                                            if int(e) == current_day and m == current_month:
                                                if m <= 9:
                                                    dates_cycled_writer(user_name, str(e), ('%02d' % m), str(last_recorded_year), price_go, price_return)
                                                else:
                                                    dates_cycled_writer(user_name, str(e), str(m), str(last_recorded_year), price_go, price_return)
                                                add_new_year(user_name, m)
                                                print("Good")
                                            else:
                                                print("Good")
            #Check if date before is on the list of dates cycled, if not add it with value 0
                                        if daily_check == "Not yet":
                                            not_yet(current_year, current_month, current_day, user_name)
                                        if daily_check == "Stop":
                                            stopper(user_name, last_recorded_year, m, e)
            #Return to start screen
                                    user_choice_1 = input("{}, your records are up to date, would you like to keep working under your name, work under any other name or exit the program(Keep name/New name/Exit)?: ".format(user_name))
                                    keepname_newname_exit(user_name, user_choice_1)

def update_dates_expended(expenses_reason, expenses_price, user_name, day, month, year):
    expenses_writer(user_name, day, month, year, expenses_reason, expenses_price)
    expenses_check = input("Did you have any other expense on that date?: ")
    if expenses_check == "Yes":
        expenses_reason = input("What else did you buy?: ")
        expenses_price = float(input("How much did it cost?: "))
        update_dates_expended(expenses_reason, expenses_price, user_name, day, month, year)
    if expenses_check == "No":
        expenses_check_2 = input("Did you have any other expense in any other date?: ")
        if expenses_check_2 == "Yes":
            expenses_reason = input("What did you buy?: ")
            expenses_price = float(input("How much did it cost?: "))
            expenses_date = input("When did you buy it(yyyy-mm-dd)?: ")
            year, month, day = map(str, expenses_date.split('-'))
            update_dates_expended(expenses_reason, expenses_price, user_name, day, month, year)
        if expenses_check_2 == "No":
            user_choice_1 = input("{}, your records are up to date, would you like to keep working under your name, work under any other name or exit the program(Keep name/New name/Exit)?: ".format(user_name))
            keepname_newname_exit(user_name, user_choice_1)

def dates_cycled_writer(user_name, day, month, year, price_go, price_return):
#Read the document    
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
#Get list of the years and the months already recorded in the records document
        list_months = []
        list_years = []
        total_saved = 0
        total_days_cycled = 0
        for key, value in records_dictionary.items():
            if key == "Dates":
                for e in value:
                    for key1, value1 in e.items():
                        list_years.append(key1)
                        if key1 == year:
                            for e1 in value1:
                                for key2, value2 in e1.items():
                                    list_months.append(key2)
#Add new year
        if year not in list_years:
            e["{}".format(year)] = [{"{}".format(month):{"{}".format(day):price_go+price_return, "Total days cycled": 1, "Total saved": price_go+price_return}}]
#Add new month 
        if year in list_years:
            if month not in list_months:
                records_dates_dictionary = dict(e)
                if type(records_dates_dictionary[year]) == list:
                    with open("{}_records.json".format(user_name), "r") as f:    
                        records_dates_dictionary[year].append({"{}".format(month):{"{}".format(day):price_go+price_return, "Total days cycled": 1, "Total saved": price_go+price_return}})
#Add new day
            if month in list_months:
                for key, value in records_dictionary.items():
                    if key == "Dates":
                        for e in value:
                            for key1, value1 in e.items():
                                if key1 == year:
                                    for e1 in value1:
                                        for key2, value2 in e1.items():
                                            if key2 == month:
                                                value2[day] = price_go+price_return
#Update total days cycled and total saved
                                                for key3, value3 in value2.items():
                                                    if key3 != "Total days cycled" and key3 != "Total saved":
                                                        total_saved = total_saved + value3
                                                        total_days_cycled = total_days_cycled + 1
                                                value2["Total days cycled"] = total_days_cycled
                                                value2["Total saved"] = total_saved
#Write dates in which the user cycle on the Dates dictionary
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Get lists of the years, months and days for sort the data
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
        years = []
        months = []
        days_and_totals = []
        for e in records_dictionary["Dates"]:
            years_in_dates_list_dict = e
            for key, value in e.items():
                years.append(key)
                if key == year:
                    months_in_year_list_dict = value
                    for e1 in value:
                        for key1, value1 in e1.items():
                            months.append(key1)
                            if key1 == month:
                                dates_in_month_dictionary = value1
                                for e2 in value1:
                                    days_and_totals.append(e2)
#Sort days    
    #Extract numbers functions
    def extract_numbers(days_and_totals):
        try:
            return str(days_and_totals)
        except KeyError:
            return 0
    #Get days sorted as a list    
    days_and_totals.sort(key=extract_numbers, reverse=False)
    days_and_totals_sorted = []
    for d in days_and_totals:
        days_and_totals_sorted.append(d)
    #Convert the list on a dictionary
    days_and_totals_sorted_dict = {}
    for date in days_and_totals_sorted:
        for key, value in dates_in_month_dictionary.items():
            if key == date:
                days_and_totals_sorted_dict.update({date:value})
    #Write on the document
    for y in records_dictionary["Dates"]:
        for key, value in y.items():
            if key == year:
                for m in value:
                    for key1, value1 in m.items():
                        if key1 == month:
                            m[month] = days_and_totals_sorted_dict
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)                
#Sort months    
    #Extract numbers functions
    def extract_numbers(months):
        try:
            return str(months)
        except KeyError:
            return 0
    #Get months sorted as a list
    months.sort(key=extract_numbers, reverse=False)
    months_sorted = []
    for m in months:
        months_sorted.append(m)
    #Convert the list on a dictionary
    months_sorted_dict = {}
    for month in months_sorted:
        for e in months_in_year_list_dict:
            for key, value in e.items():
                if key == month:
                    months_sorted_dict.update({month:value})
    #Write on the document
    for y in records_dictionary["Dates"]:
        for key, value in y.items():
            if key == year:
                y[year] = [months_sorted_dict]
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Sort years
    #Extract numbers functions
    def extract_numbers(years):
        try:
            return str(years)
        except KeyError:
            return 0
    #Get months sorted as a list
    years.sort(key=extract_numbers, reverse=False)
    years_sorted = []
    for y in years:
        years_sorted.append(y)
    #Convert the list on a dictionary
    years_sorted_dict = {}
    for year in years_sorted:
        for key, value in years_in_dates_list_dict.items():
            if key == year:
                years_sorted_dict.update({year:value})
    #Write on the document
    records_dictionary["Dates"] = [years_sorted_dict]
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Call balances writer
    balances_writer(user_name)

def expenses_writer(user_name, day, month, year, expenses_reason, expenses_price):
#Add first expense data
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
        if len(records_dictionary["Expenses"]) == 0:
            if type(records_dictionary["Expenses"]) == list:
                with open("{}_records.json".format(user_name), "r") as f:    
                    records_dictionary["Expenses"].append({"{}".format(year):[{"{}".format(month):{"{}".format(day):{"{}".format(expenses_reason):expenses_price}}}]})
#Get the list of years, months and days already registered in the document
        if len(records_dictionary["Expenses"]) != 0:
            expenses_years_list = []
            expenses_months_list = []
            expenses_days_list = []
            total_expended_per_day = 0
            for key, value in records_dictionary.items():
                if key == "Expenses":
                    for e in value:
                        for key1, value1 in e.items(): 
                            expenses_years_list.append(key1)
                            for e1 in value1:
                                for key2, value2 in e1.items():
                                    if key1 == year:
                                        expenses_months_list.append(key2)
                                        for e2 in value2:
                                            if key2 == month:
                                                expenses_days_list.append(e2)
#Add new year
            if year not in expenses_years_list:
                records_dictionary["Expenses"].append({"{}".format(year):[{"{}".format(month):{"{}".format(day):{"{}".format(expenses_reason):expenses_price,"Total expended":expenses_price}}}]})
#Add new month
            if year in expenses_years_list:
                if month not in expenses_months_list:
                    for key, value in records_dictionary.items():
                        if key == "Expenses":
                            for e in value:
                                for key1, value1 in e.items():
                                    if key1 == year:
                                        e[year].append({"{}".format(month):{"{}".format(day):{"{}".format(expenses_reason):expenses_price,"Total expended":expenses_price}}})
#Add new day
                if month in expenses_months_list:
                    if day not in expenses_days_list:
                        for key, value in records_dictionary.items():
                            if key == "Expenses":
                                for e in value:
                                    for key1, value1 in e.items():
                                        if key1 == year:
                                            for e1 in value1:
                                                for key2, value2 in e1.items():
                                                    if key2 == month:
                                                        value2[day] = {"{}".format(expenses_reason):expenses_price,"Total expended":expenses_price}
#Add to existant day
                    if day in expenses_days_list:
                        for key, value in records_dictionary.items():
                            if key == "Expenses":
                                for e in value:
                                    for key1, value1 in e.items():
                                        if key1 == year:
                                            for e1 in value1:
                                                for key2, value2 in e1.items():
                                                    if key2 == month:
                                                        for key3, value3 in value2.items():
                                                            if key3 == day:
                                                                value3[expenses_reason] = expenses_price
#Write dates in which the user has expenses on the Dates dictionary
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Update total expended
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
        total_expended_per_day = 0
        for key, value in records_dictionary.items():
            if key == "Expenses":
                for e in value:
                    for key1, value1 in e.items(): 
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key1 == year:
                                    for e2 in value2:
                                        if key2 == month:
                                            if e2 == day:
                                                for key3, value3 in value2.items():
                                                    if key3 == day:
                                                        for key4, value4 in value3.items():
                                                            if key4 != "Total expended":
                                                                total_expended_per_day = total_expended_per_day + value4
                                                                value3["Total expended"] = total_expended_per_day
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)
#Call expenses sorters
    data_for_expenses_sorters(user_name, year, month, day)
#Call balances writer
    balances_writer(user_name)

def data_for_expenses_sorters(user_name, year, month, day):
#Get lists of the years, months and days for sort the data
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
#Get the list of years, months and days already registered in the document        
        expenses_years_list = []
        expenses_months_list = []
        expenses_days_list = []
        total_expended_per_day = 0
        for key, value in records_dictionary.items():
            if key == "Expenses":
                for e in value:
                    for key1, value1 in e.items(): 
                        expenses_years_list.append(key1)
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key1 == year:
                                    expenses_months_list.append(key2)
                                    for e2 in value2:
                                        if key2 == month:
                                            expenses_days_list.append(e2)
#Get lists of the years, months and days for sort the data
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
        years = []
        months = []
        days = []
        reasons_and_totals = []
        years_in_expenses_list_dict = records_dictionary["Expenses"]
        for e in records_dictionary["Expenses"]:
            for key, value in e.items():
                years.append(key)
                if key == year:
                    months_in_year_list_dict = value
                    for e1 in value:
                        for key1, value1 in e1.items():
                            months.append(key1)
                            if key1 == month:
                                days_in_month_dictionary = value1
                                for key2, value2 in value1.items():
                                    days.append(key2)
                                    if key2 == day:
                                        reasons_and_totals_in_day_dict = value2
                                        for key3, value3 in value2.items():
                                            reasons_and_totals.append(key3)
#Call sorters in order    
    expenses_years_sorter(user_name, expenses_years_list, years_in_expenses_list_dict, year, month, day)
    expenses_months_sorter(user_name, expenses_months_list, months_in_year_list_dict, year, month, day)
    expenses_days_sorter(user_name, expenses_days_list, days_in_month_dictionary, year, month, day)
    expenses_reasons_and_totals_sorter(user_name, reasons_and_totals, reasons_and_totals_in_day_dict, year, month, day)

def expenses_years_sorter(user_name, expenses_years_list, years_in_expenses_list_dict, year, month, day):
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
    #Extract numbers functions
    def extract_numbers(expenses_years_list):
        try:
            return str(expenses_years_list)
        except KeyError:
            return 0
    #Get days sorted as a list    
    expenses_years_list.sort(key=extract_numbers, reverse=False)
    expenses_years_list_sorted = []
    for y in expenses_years_list:
        expenses_years_list_sorted.append(y)
    #Convert the list on a dictionary (retake here)
    expenses_years_list_sorted_dict = {}
    for year in expenses_years_list_sorted:
        for e in years_in_expenses_list_dict:
            for key, value in e.items():
                if key == year:
                    expenses_years_list_sorted_dict.update({year:value})
    #Write on the document
    records_dictionary["Expenses"] = [expenses_years_list_sorted_dict]
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)

def expenses_months_sorter(user_name, expenses_months_list, months_in_year_list_dict, year, month, day):
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
    #Extract numbers functions
    def extract_numbers(expenses_months_list):
        try:
            return str(expenses_months_list)
        except KeyError:
            return 0
    #Get days sorted as a list    
    expenses_months_list.sort(key=extract_numbers, reverse=False)
    expenses_months_list_sorted = []
    for m in expenses_months_list:
        expenses_months_list_sorted.append(m)
    #Convert the list on a dictionary
    expenses_months_list_sorted_dict = {}
    for month in expenses_months_list_sorted:
        for e in months_in_year_list_dict:
            for key, value in e.items():
                if key == month:
                    expenses_months_list_sorted_dict.update({month:value})
    #Write on the document
        for y in records_dictionary["Expenses"]:
            for key, value in y.items():
                if key == year:
                    y[year] = [expenses_months_list_sorted_dict]
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)

def expenses_days_sorter(user_name, expenses_days_list, days_in_month_dictionary, year, month, day):        
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
    #Extract numbers functions
    def extract_numbers(expenses_days_list):
        try:
            return str(expenses_days_list)
        except KeyError:
            return 0
    #Get days sorted as a list    
    expenses_days_list.sort(key=extract_numbers, reverse=False)
    expenses_days_list_sorted = []
    for d in expenses_days_list:
        expenses_days_list_sorted.append(d)
    #Convert the list on a dictionary
    expenses_days_list_sorted_dict = {}
    for day in expenses_days_list_sorted:
        for key, value in days_in_month_dictionary.items():
            if key == day:
                expenses_days_list_sorted_dict.update({day:value})
    #Write on the document
        for y in records_dictionary["Expenses"]:
            for key, value in y.items():
                if key == year:
                    for m in value:
                        for key1, value1 in m.items():
                            if key1 == month:
                                m[month] = expenses_days_list_sorted_dict
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)

def expenses_reasons_and_totals_sorter(user_name, reasons_and_totals, reasons_and_totals_in_day_dict, year, month, day):
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
    #Extract reasons and total function
    def extract_numbers(reasons_and_totals):
        try:
            return str(reasons_and_totals)
        except KeyError:
            return 0
    #Get days sorted as a list    
    reasons_and_totals.sort(key=extract_numbers, reverse=False)
    reasons_and_totals_sorted = []
    for r in reasons_and_totals:
        if r != "Total expended":
            reasons_and_totals_sorted.append(r)
    for r in reasons_and_totals:
        if r == "Total expended":
            reasons_and_totals_sorted.append(r)
    #Convert the list on a dictionary
    reasons_and_totals_sorted_dict = {}
    for reason in reasons_and_totals_sorted:
        for key, value in reasons_and_totals_in_day_dict.items():
            if key == reason:
                reasons_and_totals_sorted_dict.update({reason:value})
    #Write on the document
    for y in records_dictionary["Expenses"]:
        for key, value in y.items():
            if key == year:
                for m in value:
                    for key1, value1 in m.items():
                        if key1 == month:
                            value1[day] = reasons_and_totals_sorted_dict                        
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)

def balances_writer(user_name):
#Get the price of the bike    
    with open("{}.json".format(user_name), "r") as f:
        dictionary = json.load(f)
        for key, value in dictionary.items():
            if key == "Price of the bike":
                bike_price = value
#Get total saved and total days cycled per month
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
        total_days_cycled = 0
        total_saved = 0
        total_expended = 0
        for key, value in records_dictionary.items():
            if key == "Dates":
                for e in value:
                    for key1, value1 in e.items():
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                for key3, value3 in value2.items():
                                    if key3 == "Total days cycled":
                                        total_days_cycled = total_days_cycled + value3
                                    if key3 == "Total saved":
                                        total_saved = total_saved + value3
#Get total expended
            if key == "Expenses":
                for e in value:
                    for key1, value1 in e.items():
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                for key3, value3 in value2.items():
                                    for key4, value4 in value3.items():
                                        if key4 == "Total expended":
                                            total_expended = total_expended + value4
#Write data on the dictionary
        records_dictionary["Total days cycled"] = total_days_cycled
        records_dictionary["Total saved"] = total_saved
        records_dictionary["Total spent"] = total_expended
        records_dictionary["Balance"] = total_saved - (bike_price + total_expended)
    with open("{}_records.json".format(user_name), "w") as f:
        json.dump(records_dictionary, f, indent=4)

def last_date_empty_deleter(user_name):
#Delete dates with 0 value
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
        dates_not_cycled = []
        for key, value in records_dictionary.items():
            if key == "Dates":
                for e in value:
                    for key1, value1 in e.items():
                        if value1 == 0:
                            dates_not_cycled.append(key1)
        for key in dates_not_cycled:
            if key in e:
                del e[key]
    if type(records_dictionary["Dates"]) == list:
        with open("{}_records.json".format(user_name), "r") as f:
            records_dictionary["Dates"].clear()    
            records_dictionary["Dates"].append(e)
        with open("{}_records.json".format(user_name), "w+") as f:
            json.dump(records_dictionary, f, indent=4)

def stopper(user_name, year, month, day):
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
#Get the last recorded day, month and year    
    years_list = []
    months_list = []
    days_list = []
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    years_list.append(key1)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                months_list.append(key2)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key2 == months_list[-1]:
                                    for e2 in value2:
                                        if e2 != "Total days cycled" and e2 != "Total saved":
                                            days_list.append(e2)
    last_recorded_year = int(years_list[-1])
    last_recorded_month = int(months_list[-1])
    last_recorded_day = int(days_list[-1])
#Check if the day before of the iterated day had been registered, if not register it with value 0
    if datetime(last_recorded_year, last_recorded_month, last_recorded_day) == datetime(year, month, int(day)) - timedelta(days= 1):
        print("Your data has been saved, you can update it whenever you wish")
        user_choice_1 = input("Now, would you like to keep working under your name, work under any other name or exit the program (Keep name/New name/Exit)?: ".format(user_name))
        keepname_newname_exit(user_name, user_choice_1)
    else:
        date_to_print = datetime(year, month, int(day)) - timedelta(days= 1)
        dates_cycled_writer(user_name, str('{:02d}'.format(date_to_print.day)), str(date_to_print.month), str(date_to_print.year), 0, 0)
        add_new_year(user_name, date_to_print.month)
        print("Your data has been saved, you can update it whenever you wish")
        user_choice_1 = input("Now, would you like to keep working under your name, work under any other name or exit the program (Keep name/New name/Exit)?: ".format(user_name))
        keepname_newname_exit(user_name, user_choice_1)

def not_yet(current_year, current_month, current_day, user_name):
    with open("{}_records.json".format(user_name), "r") as f:    
        records_dictionary = json.load(f)
#Get the last recorded day, month and year
    years_list = []
    months_list = []
    days_list = []
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    years_list.append(key1)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                months_list.append(key2)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key2 == months_list[-1]:
                                    for e2 in value2:
                                        if e2 != "Total days cycled" and e2 != "Total saved":
                                            days_list.append(e2)
    last_recorded_year = int(years_list[-1])
    last_recorded_month = int(months_list[-1])
    last_recorded_day = int(days_list[-1])
#Check if the day before of the current day had been registered, if not register it with value 0
    if datetime(last_recorded_year, last_recorded_month, last_recorded_day) == datetime(current_year, current_month, current_day) - timedelta(days= 1):
        print("I will ask you again later")
    if datetime(last_recorded_year, last_recorded_month, last_recorded_day) != datetime(current_year, current_month, current_day) - timedelta(days= 1):
        date_to_print = datetime(current_year, current_month, current_day) - timedelta(days= 1)
        dates_cycled_writer(user_name, str('{:02d}'.format(date_to_print.day)), str(date_to_print.month), str(date_to_print.year), 0, 0)
        add_new_year(user_name, date_to_print.month)
        print("I will ask you again later")

def keepname_newname_exit(user_name, user_choice_1):
    if user_choice_1 == "Keep name":
        start_screen(user_name, user_choice_1)
    if user_choice_1 == "New name":
        user_name = input("Please, tell me your name?: ")
        start_screen(user_name, user_choice_1)
    if user_choice_1 == "Exit":
        print("See you next time, thanks {}!".format(user_name))
        exit()

def add_new_year(user_name, month):
#Read the documents
    with open("{}.json".format(user_name), "r") as f:
        dictionary = json.load(f)
    with open("{}_records.json".format(user_name), "r") as f:
        records_dictionary = json.load(f)
#Get the last recorded day, month and year
    years_list = []
    months_list = []
    days_list = []
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    years_list.append(key1)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                months_list.append(key2)
    for key, value in records_dictionary.items():
        if key == "Dates":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == years_list[-1]:
                        for e1 in value1:
                            for key2, value2 in e1.items():
                                if key2 == months_list[-1]:
                                    for e2 in value2:
                                        if e2 != "Total days cycled" and e2 != "Total saved":
                                            days_list.append(e2)
    last_recorded_year = int(years_list[-1])
    last_recorded_month = int(months_list[-1])
    last_recorded_day = int(days_list[-1])
#Get the years in data doc as a list    
    years_in_data_doc = []
    for key, value in dictionary.items():    
        if key == "Years":
            for e in value:
                for key1, value1 in e.items():
                    years_in_data_doc.append(key1)
#Get start year
    for key, value in dictionary.items():
        if key == "Starting date":
            for e in value:
                for key1, value1 in e.items():
                    if key1 == "Starting year":
                        start_year = value1
#Check if we are iterating the last month of the year
    if month == 12 and str(last_recorded_year+1) not in years_in_data_doc:
#If we are, create a list with just the upcoming year    
        new_year = list(range(start_year, last_recorded_year + 2))
        new_year_list = []
        new_year_list.append(new_year[-1])
#Get the upcoming year as a list of nested lists, where each of it has represents a month with the list of days 
        for y in new_year_list:
            months_as_list = []
            for m in range(1, 13):
                month = calendar.monthcalendar(y, m)
                flat_list = []
                for sublist in month:
                    for item in sublist:
                        flat_list.append(item)              
                no_zero_list = []
                for e in flat_list:
                    if e != 00:
                        no_zero_list.append("%02d" % e)
                months_as_list.append(no_zero_list)
#Write the upcoming year on the file
        with open("{}.json".format(user_name), "r") as f:    
            dictionary = json.load(f)
            for key, value in dictionary.items():
                if key == "Years":
                    for e in value:
                        e["{}".format(new_year[-1])] = months_as_list
        with open("{}.json".format(user_name), "w") as f:
            json.dump(dictionary, f, indent=4)    

print("Welcome to 'The cycling saves calculator'\nWith this program you will be able to track day by day\nthe money you are saving while you move around the city by bike")
print("\n")
user_name = input("Before start please, tell me your name?: ")
print("\n")
try:
    data = open("{}.json".format(user_name))
    data.close()
    records = open("{}_records.json".format(user_name))
    records.close()
    print("Hello again {}, your options are:\n - Update your database(Update)\n - Exit the program(Exit)\n".format(user_name))
    user_choice = input("What would you like to do?: ")
    if user_choice == "Update":
        print("\n")
        start_screen(user_name, user_choice)
    if user_choice == "Exit":
        print("\n")
        start_screen(user_name, user_choice)
except FileNotFoundError:
    print("Welcome {}, your options are:\n - Create a new database(Create)\n - Exit the program(Exit)\n".format(user_name))
    user_choice = input("What would you like to do?: ")
    if user_choice == "Create":
        print("\n")
        start_screen(user_name, user_choice)
    if user_choice == "Exit":
        print("\n")
        start_screen(user_name, user_choice)
    



