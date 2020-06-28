import sqlite3
import os
import datetime
import pprint
from string import punctuation


database_file = 'projects.db'
history_save = 'history.txt'


def create_file(filename):
    with open(file=filename, mode="w") as file:
        file.close()


def db_connection(db_file):
    db = sqlite3.connect(db_file)
    return db


def create_table(conn):
    sql_table_create_query = """ CREATE TABLE IF NOT EXISTS main_projects (
                                            name TEXT, 
                                            project_describe TEXT, 
                                            importance INTEGER, 
                                            status TEXT,
                                            PRIMARY KEY("name")
                                        ); """

    try:
        c = conn.cursor()
        c.execute(sql_table_create_query)
    except sqlite3.Error as e:
        print(e)


def check_file_exists(filename):
    exists = os.path.isfile(filename)
    if exists:
        pass
    else:
        print('[WARNING] No database file was found ! \nCreating database file.')
        create_file(filename=filename)
        db_conn = db_connection(db_file=filename)
        create_table(conn=db_conn)
        return db_conn


def insert_project(conn, name, description, importance, status):
    cursor = conn.cursor()
    check_name_exists(conn, name)
    query = f"INSERT INTO main_projects {name}, {description}, {importance}, {status}"
    cursor.execute('''INSERT INTO main_projects(name, project_describe, importance, status) VALUES(?, ?, ?, ?)''', (name, description, importance,
                                                                                                                    status))
    conn.commit()
    print("\nData successfully inserted.\n")
    conn.close()
    return str(query)


def show_all_projects(conn):
    cur = conn.cursor()
    query = f"SELECT * FROM main_projects WHERE status = in_progress ORDER BY importance DESC"
    cur.execute('''SELECT * FROM main_projects WHERE status = "in_progress" ORDER BY importance DESC''')
    rows = cur.fetchall()
    print("\n")
    print("AVAILABLE PROJECTS:")
    [print(row) for row in rows]
    print("\n")
    conn.close()
    return query


def check_option(option_value):
    if not option_value.isnumeric():
        print("[WARNING] Given value must be an integer.")
        show_menu()
    if int(option_value) not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("[WARNING] You chose an option that does not exist.")
        show_menu()
    return int(option_value)


def check_project_importance(option_value):
    if not option_value.isnumeric():
        print("[WARNING] Given value must be an integer.")
        show_menu()
    return option_value


def update_task(conn, name, project_describe):
    cur = conn.cursor()
    query = f"UPDATE main_projects SET project_describe = {name} WHERE name = {project_describe}"
    cur.execute('''UPDATE main_projects SET project_describe = (?) WHERE name = (?)''', (project_describe, name))
    print(f"Successfully changed {name} project description.\n")
    conn.commit()
    conn.close()
    return query


def update_importance(conn, name, importance):
    cur = conn.cursor()
    query = f"UPDATE main_projects SET importance = {name} WHERE name = {importance}"
    cur.execute('''UPDATE main_projects SET importance = (?) WHERE name = (?)''', (importance, name))
    print(f"Successfully changed {name} project importance.\n")
    conn.commit()
    conn.close()
    return query


def retire_project(conn, name):
    retirement = "done"
    cur = conn.cursor()
    query = f"UPDATE main_projects SET status = {retirement} WHERE name = {name}"
    cur.execute('''UPDATE main_projects SET status = ? WHERE name = ?''', (retirement, name))
    print(f"Successfully retired {name} project.\n")
    conn.commit()
    conn.close()
    return query


def show_done_projects(conn):
    cur = conn.cursor()
    query = "SELECT * FROM main_projects WHERE status = done ORDER BY importance DESC"
    cur.execute('''SELECT * FROM main_projects WHERE status = "done" ORDER BY importance DESC''')
    rows = cur.fetchall()
    print("\n")
    print("DONE PROJECTS:")
    [print(row) for row in rows]
    print("\n")
    conn.close()
    return query


def delete_all_tasks(conn):
    print("[WARNING] You are going to DELETE all the data !!!")
    cur = conn.cursor()
    cur.execute('DELETE FROM main_projects')
    conn.commit()
    conn.close()
    query = "DELETE FROM main_projects"
    print("\n")
    print("Data successfully deleted.")
    print("\n")
    return query


def bye_bye_info():
    bye_info = "Close"
    print("Closing the program. ............... \nYou successfully exited the program. \nBYE BYE")
    return bye_info


def save_history(query):
    save_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.txt", 'a+') as history_file:
        history_file.write((query + "; " + str(save_data) + "\n"))


def show_history():
    with open(history_save, 'r') as save_file:
        text = save_file.readlines()
    print("\n")
    print("PRINTING HISTORY ..........")
    pprint.pprint(text)
    print("\n")


def strip_punctuation(string):
    return ''.join(char for char in string if char not in punctuation)


def check_name_exists(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT name FROM main_projects')
    rows = cur.fetchall()
    names = [strip_punctuation(str(i).lower()) for i in rows]

    if name.lower() in names:
        print("\n")
        print("Given project name already exists.")
        print("Returning to main menu.\n")
        show_menu()
    else:
        print("Name acceptable.")


def show_menu():
    menu_loop = 1
    while menu_loop == 1:
        print("[ ---- MENU ---- ]")
        print("[1] Add new project.")
        print("[2] Show all projects.")
        print("[3] Change project description.")
        print("[4] Change project importance.")
        print("[5] Mark project as done.")
        print("[6] Show done projects.")
        print("[7] <Delete all data>")
        print("[8] Show history.")
        print("[9] Exit program.\n")

        option = input("Enter an option: ")
        option = check_option(option)

        if option == 1:
            check_file_exists(filename=database_file)

            project_name = input("Enter project name: ")
            project_describe = input("Enter project description: ")
            project_importance = input("Enter the importance of project (integer): ")
            project_importance = check_project_importance(project_importance)

            insert_query = insert_project(conn=db_connection(db_file=database_file), name=project_name, description=project_describe,
                                          importance=project_importance, status='in_progress')
            save_history(insert_query)
        elif option == 2:
            check_file_exists(filename=database_file)

            show_query = show_all_projects(conn=db_connection(db_file=database_file))
            save_history(show_query)
        elif option == 3:
            check_file_exists(filename=database_file)

            name_to_change = input("Enter project name which description you want to change: ")
            project_description = input("Enter new description: ")
            update_query = update_task(conn=db_connection(db_file=database_file), name=name_to_change, project_describe=project_description)
            save_history(update_query)
        elif option == 4:
            check_file_exists(filename=database_file)

            name_to_change = input("Enter project name which importance you want to change: ")
            importance_to_change = input("Enter level of importance: ")
            update_query = update_importance(conn=db_connection(db_file=database_file), name=name_to_change, importance=importance_to_change)
            save_history(update_query)
        elif option == 5:
            name_to_retire = input("Enter project name which you want to mark as done: ")
            retire_query = retire_project(conn=db_connection(db_file=database_file), name=name_to_retire)
            save_history(retire_query)
        elif option == 6:
            check_file_exists(filename=database_file)

            show_query = show_done_projects(conn=db_connection(db_file=database_file))
            save_history(show_query)
        elif option == 7:
            check_file_exists(filename=database_file)

            delete_query = delete_all_tasks(conn=db_connection(db_file=database_file))
            save_history(delete_query)
        elif option == 8:
            show_history()
        elif option == 9:
            menu_loop = 0
            bye_query = bye_bye_info()
            save_history(bye_query)
