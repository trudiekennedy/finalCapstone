# ===== IMPORTING LIBRARIES ===========
# This is the section where you will import libraries.
import datetime  # to handle dates in tasks - reference: https://www.w3schools.com/python/python_datetime.asp

# ===== PROGRAM VARIABLES ===== These variables are used throughout program so are initialised in outer scope.
decorative_line = "-" * 80  # Prints '-' 80 times to help with formatting of display & reports.
short_decorative_line = "-" * 36    # Prints a shorter line to help with formatting.
logged_in_user = ""  # Stores who user is after they successfully log in.
current_date = datetime.datetime.today().date()     # Stores today's date to be used in comparisons & creation date.
user_credentials_dict = {}      # Dictionary to help validate credentials when logging in & registering users.
task_dict = {}      # Dictionary to store tasks.
stat_dict = {}     # Dictionary to store user stats.


# ===== PROGRAM FUNCTIONS =====
# Opens user.txt & loops through each line: strips "\n" & ", " then adds username & password to "user_credentials_dict".
def import_users_to_dict():
    with open("user.txt", "r") as file:
        for user in file:
            user = user.strip("\n").split(", ")
            user_credentials_dict[user[0]] = user[1]


# Opens tasks.txt, loops through each line: strips "\n" & ", ".
# Each task becomes a dictionary within "task_dict" variable; the "counter" variable will serve to name each dictionary.
# Each index of the split line is assigned to a key describing the value within the "counter" named dictionary.
def import_tasks_to_dict():
    with open("tasks.txt", "r") as tasks_file:
        counter = 0
        for lines in tasks_file:
            counter += 1
            lines = lines.strip("\n").split(", ")
            task_dict[counter] = {"Summary": lines[1],
                                  "Assigned to": lines[0],
                                  "Assigned on": lines[3],
                                  "Due": lines[4],
                                  "Completed": lines[5],
                                  "Description": lines[2]}


# Register user function
def reg_user():
    # Calls import users function.  User asked to input username & password for the new user.
    # If username already exists, user is asked to try again until they pick a unique username.
    import_users_to_dict()
    while True:
        new_username = input("Please enter a username: ").lower()
        if new_username in user_credentials_dict:
            print(f"Username already in use. Please try again.\n"
                  f"{decorative_line}\n")
            continue

        # User is asked to input password & then confirm the password.
        # If passwords don't match, user is told to try again: if they match, new user is registered & dict is updated.
        new_password = input("Please enter a password: ")
        confirm_password = input("Confirm password: ")

        if new_password != confirm_password:
            print(f"Password mismatch. Please try again.\n")
        else:
            with open('user.txt', "a") as users_file:
                users_file.write(f"\n{new_username}, {new_password}")
                return (f"\nSuccess! You have registered {new_username}.\n"
                        f"{decorative_line}")


# Add task function.
def add_task():
    # "new_key" declared storing the length of task_dict + 1 to determine name of new dictionary.
    new_key = len(task_dict) + 1
    task_dict[new_key] = {}

    # Asks user to input title & description then assigns to the "new_key" named dictionary in "task_dict".
    task_dict[new_key]['Summary'] = input("Task title: ")
    task_dict[new_key]['Description'] = input("Task description: ")

    # Asks user to input a username to assign task to, checks username is valid before assigning to dictionary.
    import_users_to_dict()
    while True:
        assign_to = input("Who should this task be assigned to? (username): ").lower()
        if assign_to not in user_credentials_dict:
            print(f"Username is not recognised. Please try again.\n"
                  f"{decorative_line}")
            continue
        task_dict[new_key]['Assigned to'] = assign_to
        break

    # Assigns current date to "new_key" dictionary within "tasks_dict" as the date task is created.
    # Asks user to input a due date, formats date and assigns to dictionary.
    task_dict[new_key]['Assigned on'] = current_date
    print(f"Current date: {task_dict[new_key]['Assigned on']}")
    print("When does this task need to be done by? (DD-MM-YYYY)")
    due_date_day, due_date_month, due_date_year = int(input("DD: ")), int(input("MM: ")), int(input("YYYY: "))
    task_dict[new_key]['Due'] = datetime.date(due_date_year, due_date_month, due_date_day).strftime("%d %b %Y")
    task_dict[new_key]["Completed"] = "No"  # Saved as value in dictionary to show task not complete yet.

    # Appends all values in "new_key" dictionary within "tasks_dict" to the "tasks.txt" file & displays message to user.
    with open("tasks.txt", "a") as taskman_file:
        taskman_file.write(f"{task_dict[new_key]['Assigned to']}, "
                           f"{task_dict[new_key]['Summary']}, "
                           f"{task_dict[new_key]['Description']}, "
                           f"{task_dict[new_key]['Assigned on']}, "
                           f"{task_dict[new_key]['Due']}, "
                           f"{task_dict[new_key]['Completed']}")
        return f"\nSuccess! Your task has been submitted.\n" \
               f"{decorative_line}"


# Print task function to pull & display information from "task_dict" depending on the argument passed as the key value.
def print_task(task):
    print(f"TASK-{task}"
          f"\nTask Summary:\t{task_dict[task]['Summary']}"
          f"\nAssigned to:\t{task_dict[task]['Assigned to']}"
          f"\nAssigned on:\t{task_dict[task]['Assigned on']}"
          f"\nDue date:\t\t{task_dict[task]['Due']}"
          f"\nCompleted:\t\t{task_dict[task]['Completed']}"
          f"\nDescription:\t{task_dict[task]['Description']}"
          f"\n{decorative_line}")


# View all function that imports info from "tasks.txt", loops through each line & displays the info in the task.
def view_all():
    import_tasks_to_dict()
    for task in task_dict:
        print_task(task)


# Function imports "tasks.txt" to "tasks_dicts" & displays each task that is assigned "current_user".
def view_mine(current_user):
    import_tasks_to_dict()
    current_user_task_count = 0
    for task in task_dict:
        if current_user == task_dict[task]['Assigned to']:
            print_task(task)
            current_user_task_count += 1
    if current_user_task_count == 0:
        print("You don't have any tasks assigned to you! Please check back later.")


# Function to update assignee of a task based on arguments being passed for task number and the new assignee's username.
def reassign_task(number, new_assignee):
    task_dict[number]['Assigned to'] = new_assignee
    return f"TASK-{number} has been reassigned to {new_assignee}"


# Function to provide various edit options of a task: user can mark as completed or edit their task.
def task_options():
    while True:
        view_mine_menu = input(f"What would you like to do with this task?"
                               f"\ne\t-\tedit task"
                               f"\nmc\t-\tmark task completed"
                               f"\nOption: ").lower()

        # If user selects e (for edit), they are given the option to reassign task or change the due date.
        if view_mine_menu == "e":
            while True:
                task_option = input(f"\n--- EDIT OPTIONS ---"
                                    f"\nrt\t-\treassign task"
                                    f"\nd\t-\tchange due date"
                                    f"\nOption: ").lower()

                # If rt (reassign) selected, user prompted to enter new assignee: program validates new assignee exists.
                if task_option == "rt":
                    assign_to = input("Who do you want to reassign this task to? ").lower()
                    if assign_to not in user_credentials_dict:
                        print(f"Sorry - action not completed: {assign_to} isn't a valid user."
                              f"\n{decorative_line}")
                        break
                    # If assignee exists, reassign_task() is called, passing "chosen_task" & "assign_to" as arguments.
                    else:
                        print(reassign_task(chosen_task, assign_to))
                        return

                # If user selects "d" (change date). They'll be shown current due date and asked to input new date.
                # New date will be formatted and then updated in "task_dict".
                elif task_option == "d":
                    print(f"The current due date of TASK-{chosen_task} is {task_dict[chosen_task]['Due']}."
                          f"\nWhat is the new due date? (DD/MM/YYYY)")
                    new_date_d, new_date_mth, new_date_yr = int(input("DD: ")), int(input("MM: ")), int(input("YYYY: "))
                    new_date = datetime.date(new_date_yr, new_date_mth, new_date_d).strftime("%d %b %Y")
                    task_dict[chosen_task]['Due'] = new_date
                    print(f"Due date has been updated to: {new_date}")
                    return

                else:
                    print(f"Invalid selection. Please try again."
                          f"\n{decorative_line}")

        # If user selects "mc" (mark complete), the "No" value saved in "Completed" key will be updated to "Yes".
        elif view_mine_menu == "mc":
            task_dict[chosen_task]['Completed'] = "Yes"
            print(f"TASK-{chosen_task} has been marked as complete."
                  f"\n{decorative_line}")
            break
        else:
            print(f"Invalid selection. Please try again."
                  f"\n{decorative_line}")


# Function calls import_tasks_to_dict() & declares variables for total tasks, complete tasks, incomplete & overdue tasks
def generate_task_report():
    import_tasks_to_dict()

    total_tasks = len(task_dict)    # Number of tasks found by determining how many dictionaries in "task_dict".
    completed_tasks = 0
    incomplete_tasks = 0
    incomplete_overdue_tasks = 0

    # Loops through each task: counts completed tasks, incomplete tasks & incomplete tasks that are overdue.
    for task in task_dict:
        if task_dict[task]["Completed"] == "Yes":
            completed_tasks += 1
        elif task_dict[task]["Completed"] == "No":
            incomplete_tasks += 1
            if current_date > datetime.datetime.strptime(task_dict[task]["Due"], "%d %b %Y").date():
                incomplete_overdue_tasks += 1

    # Works out the percentage of tasks that are incomplete & percentage that are overdue & incomplete.
    incomplete_percentage = 100 * incomplete_tasks / total_tasks
    overdue_percentage = 100 * incomplete_overdue_tasks / total_tasks

    # Writes info stored in function variables, formatted as a report to the file "task_overview.txt".
    with open("task_overview.txt", "w") as overview_file:
        overview_file.write(f"{short_decorative_line}\n"
                            f"------- TASK OVERVIEW REPORT -------\n"
                            f"------ Generated: {current_date} ------\n"
                            f"{short_decorative_line}\n"
                            f"CREATED & COMPLETED\n"
                            f"Total tasks tracked in app:\t\t{total_tasks}\n"
                            f"Total tasks completed:\t\t\t{completed_tasks}\n"
                            f"{short_decorative_line}\n"
                            f"INCOMPLETE & OVERDUE\n"
                            f"Total tasks outstanding:\t\t{incomplete_tasks}\n"
                            f"Percentage outstanding:\t\t\t{round(incomplete_percentage)}%\n"
                            f"Total tasks that are overdue:\t{incomplete_overdue_tasks}\n"
                            f"Percentage overdue:\t\t\t\t{round(overdue_percentage)}%\n"
                            f"{short_decorative_line}")


# Function to generate a user overview report
def generate_user_report():
    import_users_to_dict()  # Imports "user.txt" to "user_credentials_dict" to ensure dictionary is up-to-date.
    import_tasks_to_dict()  # Imports "tasks.txt" to "task_dict" to ensure dictionary is up-to-date.

    total_users = len(user_credentials_dict)    # Determines total number of users of the program.
    total_tasks = len(task_dict)                # Determines total number of tasks tracked by the program.

    # Writes general overview info to a file called "user_overview.txt" in a report-type format.
    with open("user_overview.txt", "w") as overview_file:
        overview_file.write(f"{short_decorative_line}\n"
                            f"------- USER OVERVIEW REPORT -------\n"
                            f"------ Generated: {current_date} ------\n"
                            f"{short_decorative_line}\n"
                            f"PROGRAM OVERVIEW\n"
                            f"Number of registered users:\t\t{total_users}\n"
                            f"Total tasks tracked in app:\t\t{total_tasks}\n"
                            f"{short_decorative_line}\n"
                            f"--------- INDIVIDUAL STATS ---------\n"
                            f"{short_decorative_line}\n")

        # Outer loop runs through each user in the "user_credentials_dict" & declares "stats_dict": within "stats_dict"
        # each user will be a dictionary with keys: "Assigned", "Completed", "Incomplete", "Overdue" (initial values: 0)
        for user in user_credentials_dict:
            stat_dict[user] = {"Assigned": 0,
                               "Completed": 0,
                               "Incomplete": 0,
                               "Overdue": 0}
            # Loops through each task and counts how many are assigned to user & how many are assigned, completed etc...
            for task in task_dict:
                if task_dict[task]["Assigned to"] == user:
                    stat_dict[user]["Assigned"] += 1
                    if task_dict[task]["Completed"] == "No":
                        stat_dict[user]["Incomplete"] += 1
                        if current_date > datetime.datetime.strptime(task_dict[task]["Due"], "%d %b %Y").date():
                            stat_dict[user]["Overdue"] += 1
                    if task_dict[task]["Completed"] == "Yes":
                        stat_dict[user]["Completed"] += 1

            # The stats for each individual (total, % assigned, completed, incomplete & overdue) are written to file.
            overview_file.write(f"{user.upper()} STATS\n")
            if stat_dict[user]['Assigned'] != 0:
                overview_file.write(f"Total program tasks assigned:\t{stat_dict[user]['Assigned']}\n"
                                    f"% of program tasks assigned:"
                                    f"\t{round(100 * stat_dict[user]['Assigned'] / total_tasks)}%\n"
                                    f"% completed:\t\t\t\t\t"
                                    f"{round(100 * stat_dict[user]['Completed'] / stat_dict[user]['Assigned'])}%\n"
                                    f"% incomplete:\t\t\t\t\t"
                                    f"{round(100 * stat_dict[user]['Incomplete'] / stat_dict[user]['Assigned'])}%\n"
                                    f"% incomplete & overdue:\t\t\t"
                                    f"{round(100 * stat_dict[user]['Overdue'] / stat_dict[user]['Assigned'])}%\n"
                                    f"{short_decorative_line}\n")
            else:   # To avoid a zero divisible error which occurs if a user hasn't been assigned any tasks.
                overview_file.write(f"No tasks assigned to this user yet!\n"
                                    f"{short_decorative_line}\n")


# ====LOGIN SECTION====
# Loop asks user for username and password whilst the combination isn't found in "user_credentials_dict".
# If credentials match, "logged_in_user" is updated with username and success message displays to user
import_users_to_dict()
while True:
    print("--- LOG IN ---")
    username = input("Username: ")
    password = input("Password: ")
    if username not in user_credentials_dict:
        print("Your username and/or password are incorrect. Please try again.")
        continue
    elif user_credentials_dict[username] == password:
        logged_in_user = username
        print(f"{decorative_line}"
              f"\nSuccess! You're logged in as {username}.\n"
              f"{decorative_line}")
        break
    else:
        print("Your username and/or password are incorrect. Please try again.")
        continue

while True:
    # Presents the menu to the user depending on who "logged_in_user" is.
    # Makes sure that the user input is converted to lower case.
    print("--- MENU ---")
    if logged_in_user == "admin":  # Admin menu.
        menu = input(f"Select one of the following options below:\n"
                     f"r\t-\tRegister a user\n"
                     f"a\t-\tAdd a task\n"
                     f"va\t-\tView all tasks\n"
                     f"vm\t-\tView my tasks\n"
                     f"gr\t-\tGenerate reports\n"
                     f"s\t-\tDisplay Statistics\n"
                     f"e\t-\tExit\n"
                     f"Option:\t").lower()
    else:  # Non-admin menu.
        menu = input(f"Select one of the following options below:\n"
                     f"r\t-\tRegister a user\n"
                     f"a\t-\tAdd a task\n"
                     f"va\t-\tView all tasks\n"
                     f"vm\t-\tView my tasks\n"
                     f"e\t-\tExit\n"
                     f"Option:\t").lower()

    if menu == "r":  # Checks "logged_in_user" is admin & if so, calls "reg_user()" function: else, displays an error.
        print(f"{decorative_line}\n"
              f"--- REGISTER USER ---\n"
              f"{decorative_line}")

        if logged_in_user == "admin":
            print(reg_user())
        else:
            print(f"You don't have permission to register users.\n"
                  f"Please add a task for admin to register the user instead.\n"
                  f"{decorative_line}")

    elif menu == "a":  # Add a task selected_email calls the "add_task()" function.
        print(f"{decorative_line}"
              f"\n--- ADD A TASK ---"
              f"\n{decorative_line}")
        print(add_task())

    elif menu == "va":  # View all tasks calls "view_all()" function.
        print(f"{decorative_line}\n"
              f"--- VIEW ALL TASKS ---\n"
              f"{decorative_line}")
        view_all()

    elif menu == "vm":  # View my tasks calls the "view_mine()" function.
        print(f"{decorative_line}\n"
              f"--- MY TASKS ---\n"
              f"{decorative_line}")

        view_mine(logged_in_user)

        # Asks user to select a task or exit view mine menu. If number selected is between 1 and number of tasks:
        # program checks selected task is assigned to user & incomplete: if so, displays task & calls "tasks_options()"
        while True:
            chosen_task = int(input(f"Choose a task number to edit or enter -1 to exit: "))
            print(f"{decorative_line}")
            if 0 < chosen_task <= len(task_dict):
                if logged_in_user == task_dict[chosen_task]['Assigned to']:
                    if task_dict[chosen_task]['Completed'] == "No":
                        print(f"{decorative_line}")
                        print_task(chosen_task)
                        task_options()

                    else:   # If selected task is complete, program doesn't offer edit options.
                        print(f"There are no edit options available for TASK-{chosen_task} "
                              f"as it has already been completed."
                              f"\n{decorative_line}")

                else:       # If selected task is not assigned to "logged_in_user", program doesn't offer edit options.
                    print(f"TASK-{chosen_task} has not been assigned to you. Please try again."
                          f"\n{decorative_line}")

            # If user chooses -1 (exit menu), updated "task_dict" is written to "tasks.txt".
            elif chosen_task == -1:
                with open("tasks.txt", "w+") as updated_file:
                    for entry in task_dict:
                        updated_file.write(f"{task_dict[entry]['Assigned to']}, "
                                           f"{task_dict[entry]['Summary']}, "
                                           f"{task_dict[entry]['Description']}, "
                                           f"{task_dict[entry]['Assigned on']}, "
                                           f"{task_dict[entry]['Due']}, "
                                           f"{task_dict[entry]['Completed']}\n")
                break
            else:
                print("This option isn't recognised. Please try again.")

    elif menu == "gr":  # Calls functions: "generate_task_report()" & "generate_user_report" if logged_in_user is admin.
        if logged_in_user == "admin":
            print(f"{decorative_line}\n"
                  f"--- GENERATE REPORTS ---")
            generate_task_report()
            generate_user_report()
            print(f"The following reports have been generated:\n"
                  f"- Task overview\n"
                  f"- User overview\n"
                  f"{decorative_line}")

        else:   # If user is not admin, reports are not generated and error is displayed.
            print(f"{decorative_line}\n"
                  f"You've entered an invalid selection. Please try again.\n"
                  f"{decorative_line}")

    elif menu == "s":  # Statistics
        # Checks "logged_in_user" is admin before calling "generate_task_report()" and "generate_user_report()".
        if logged_in_user == "admin":
            print(f"\n"
                  f"--- STATISTICS ---")
            generate_task_report()
            generate_user_report()

            # Opens files "task_overview.txt" and "user_overview.txt" and displays the reports to the user.
            with open("task_overview.txt", "r") as task_report:
                task_report = task_report.read()
                print(task_report)

            with open("user_overview.txt", "r") as user_report:
                user_report = user_report.read()
                print(user_report)

        else:  # If user isn't admin, an error is displayed.
            print(f"{decorative_line}\n"
                  f"You've entered an invalid selection. Please try again.\n"
                  f"{decorative_line}")

    elif menu == "e":  # Exits program.
        print(f"{decorative_line}\n"
              f"Goodbye, {logged_in_user} - see you soon!\n"
              f"{decorative_line}")
        exit()

    else:  # Error message is displayed if user selects unsupported option from main menu.
        print(f"{decorative_line}\n"
              f"You've entered an invalid selection. Please try again.\n"
              f"{decorative_line}")
