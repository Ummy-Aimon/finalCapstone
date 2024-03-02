
import os
import datetime


def login():
    """
    Handles user login.

    Prompts for username and password and checks against registered users in 'user.txt'.
    If credentials match, login is successful.
    """
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open("user.txt", "r") as user_file:
            users = user_file.readlines()
            for user in users:
                user_data = user.strip().split(",")
                if len(user_data) == 2:
                    admin, pass11 = user_data
                if username == admin and password == pass11:
                    print("Login successful!")
                    return username
            else:
                print("Invalid username or password. Please try again.")


def reg_user():
    """
    Registers a new user.

    Prompts for a new username and password and saves them to 'user.txt'.
    Checks if the username already exists to prevent duplicates.
    """
    username = input("Enter a new username: ")
    with open("user.txt", "r") as user_file:
        users = user_file.readlines()
        user_exists = any(username in user for user in users)
    if user_exists:
        print("Username already exists. Please choose a different username.")
    else:
        password = input("Enter a password: ")
        with open("user.txt", "a") as user_file:
            user_file.write(username + "," + password + "\n")
        print(f"User {username} registered successfully!")


def add_task():
    """
    Adds a new task to 'tasks.txt'.

    Prompts for task details (assigned user, title, description, due date) and saves them.
    """
    task_username = input("Enter the username of the person the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    task_due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
    task_completed = "No"
    with open("tasks.txt", "a") as tasks_file:
        tasks_file.write(f"{task_username},{task_title},{task_description},{task_due_date},{task_completed}\n")
    print("Task added successfully!")


def view_all():
    """
    Displays all tasks in 'tasks.txt'.

    Reads tasks and prints details for each task.
    """
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()
        if not tasks:
            print("No tasks found.")
        else:
            print("All Tasks:")
            print("-----------")
            for index, task in enumerate(tasks,1):
                        task_data = task.strip().split(",")
                        if len(task_data) >= 5:  # Ensure task_data has at least 5 elements
                            print(f"Task {index}:")
                            print(f"Assigned to: {task_data[0]}")
                            print(f"Title: {task_data[1]}")
                            print(f"Description: {task_data[2]}")
                            print(f"Due Date: {task_data[3]}")
                            print(f"Completed: {task_data[4]}")
                            print()

def view_mine(username):
    """
    Displays tasks assigned to the logged-in user.

    Reads 'tasks.txt' and filters tasks by the current user's username.
    Allows editing and marking tasks as complete.
    """
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()
        user_tasks = [task.strip() for task in tasks if username == task.split(",")[0]]
        if not user_tasks:
            print("No tasks assigned to you.")
        else:
            for index, task in enumerate(user_tasks, 1):
                task_data = task.split(",")
                print(f"Task {index}:")
                print(f"Title: {task_data[1]}")
                print(f"Description: {task_data[2]}")
                print(f"Due Date: {task_data[3]}")
                print(f"Completed: {task_data[4]}")
                print()
            edit_task(user_tasks)


def edit_task(username,user_tasks):
    """
    Edits or marks a task as complete.

    Allows the user to select a task to edit or mark as complete based on user input.
    """
    task_choice = int(
        input("Enter the number of the task you want to edit or mark as complete (-1 to return to the main menu): "))
    if task_choice == -1:
        return
    selected_task = user_tasks[task_choice - 1]
    task_data = selected_task.split(",")
    if task_data[4].lower() == "yes":
        print("Task has already been completed and cannot be edited.")
    else:
        action = input(
            "Do you want to mark the task as complete (enter 'mark') or edit the task (enter 'edit')? ").lower()
        if action == "mark":
            task_data[4] = "Yes"
            print("Task marked as complete.")
        elif action == "edit":
            new_assignee = input("Enter the new assignee's username: ")
            new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
            task_data[0] = new_assignee
            task_data[3] = new_due_date
            print("Task edited successfully.")
        else:
            print("Invalid action.")
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()
    tasks[tasks.index(selected_task)] = ",".join(task_data) + "\n"
    with open("tasks.txt", "w") as tasks_file:
        tasks_file.writelines(tasks)



    """
    Generates reports for tasks and users.

    Creates 'task_overview.txt' and 'user_overview.txt' with statistics on tasks and users.
    """
    # Implement report generation logic here (similar to the initial explanation)

def generate_reports():
    # Load tasks and calculate statistics
    with open("tasks.txt", "r") as file:
        tasks_lines = file.readlines()

    tasks = [task.strip().split(", ") for task in tasks_lines]

    total_tasks = len(tasks)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    current_date = datetime.datetime.now()

    for task in tasks:
        # Ensure task has all required elements (assuming at least 6 elements are needed)
        if len(task) < 6:
            print(f"Skipping task due to unexpected format: {task}")
            continue

        due_date_str = task[4]
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError as e:
            print(f"Error parsing date for task {task}: {e}")
            continue

        if task[5] == "Yes":
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            if due_date < current_date:
                overdue_tasks += 1

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks else 0
    # Write task_overview.txt
    with open("task_overview.txt", "w") as file:
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {completed_tasks}\n")
        file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Total number of tasks that haven’t been completed and are overdue: {overdue_tasks}\n")
        file.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")
        file.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n")

    # Load users and prepare for user-specific statistics
    with open("user.txt", "r") as file:
        users = [user.strip().split(", ") for user in file.readlines()]

    total_users = len(users)
    tasks_per_user = {user[0]: 0 for user in users}
    completed_per_user = {user[0]: 0 for user in users}
    overdue_per_user = {user[0]: 0 for user in users}

    for task_string in tasks:
        # Assuming tasks are strings separated by commas, split each one
        task_details = task_string   # Adjust based on your actual data separator

        # Ensure that task_details has at least 6 elements ([0] through [5])
        if len(task_details) >= 6:
            assignee = task_details[0].strip()  # Adjust index if necessary

            # Initialize dictionary entries if they don't exist
            if assignee not in tasks_per_user:
                tasks_per_user[assignee] = 0
                completed_per_user[assignee] = 0
                overdue_per_user[assignee] = 0

            tasks_per_user[assignee] += 1

            # Now safely check the completion status and due date
            if task_details[5].strip() == "Yes":  # Ensure to strip() if whitespace might be present
                completed_per_user[assignee] += 1
            else:
                try:
                    due_date = datetime.datetime.strptime(task_details[4].strip(), "%Y-%m-%d")
                    if due_date < current_date:
                        overdue_per_user[assignee] += 1
                except ValueError:
                    # Handle or log the error if the date format is incorrect
                    print(f"Error parsing date for task: {task_string}")

    # Write user_overview.txt
    with open("user_overview.txt", "w") as file:
        file.write(f"Total number of users: {total_users}\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        for user in users:
            username = user[0]
            total_assigned = tasks_per_user[username]
            completed = completed_per_user[username]
            overdue = overdue_per_user[username]
            incomplete = total_assigned - completed
            file.write(f"\nUser: {username}\n")
            file.write(f"Total number of tasks assigned: {total_assigned}\n")
            file.write( f"Percentage of the total number of tasks assigned: {(total_assigned / total_tasks) * 100:.2f}%\n")
            file.write(f"Percentage completed: {(completed / total_assigned) * 100 if total_assigned else 0:.2f}%\n")
            file.write(f"Percentage incomplete: {(incomplete / total_assigned) * 100 if total_assigned else 0:.2f}%\n")
            file.write(f"Percentage of tasks overdue: {(overdue / total_assigned) * 100 if total_assigned else 0:.2f}%\n")

def display_statistics():
    try:
        with open("task_overview.txt", "r") as task_overview_file:
            print("Task Overview:")
            print(task_overview_file.read())
    except FileNotFoundError:
        print("Task overview file not found. Please generate reports first.")

    try:
        with open("user_overview.txt", "r") as user_overview_file:
            print("User Overview:")
            print(user_overview_file.read())
    except FileNotFoundError:
        print("User overview file not found. Please generate reports first.")

def main():
    """
    Main function to run the task manager program.

    Handles user login, menu display, and function calls based on user input.
    """
    username = login()  # Perform user login
    if username is None:
        return
    while True:
        print("\n===== Task Manager Menu =====")
        print("0. Register User (Enter 'r')")
        print("2. Add Task (Enter 'a')")
        print("3. View All Tasks (Enter 'va')")
        print("4. View My Tasks (Enter 'vm')")
        print("5. Generate Reports (Enter 'gr')")
        print("6. Display Statistics (Enter 'ds')")
        print("7. Exit (Enter 'x')")

        choice = input("Enter your choice: ").lower()

        if choice == 'r':
            reg_user()
        elif username and choice == 'a':
            add_task()
        elif username and choice == 'va':
            view_all()
        elif username and choice == 'vm':
            view_mine(username)  # Pass the logged-in username to view_mine function
        elif username and choice == 'gr':
            generate_reports()
            print("Reports generated successfully!")
        elif choice == 'ds':
            display_statistics()
        elif choice == 'x':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

