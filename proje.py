import PySimpleGUI as sg
import sqlite3
import datetime as dt
# Database file path
db_file = 'datayogi_implementation_stage.db'

sg.set_options(font=("Helvetica", 12))
sg.theme('DarkPurple4')
# login layout
def create_login_window():
    layout = [
        [sg.Text('Email'), sg.Input(key='email')],
        [sg.Text('Password'), sg.Input(key='password', password_char='*')],
        [sg.Button('Login as Admin'), sg.Button('Login as User'), sg.Button('Cancel')],
        [sg.Button('Sign Up', font=("Helvetica", 12), key=("Sign Up"))],
    ]
    return sg.Window('DataYogiFiLmCeHeNnEmi', layout, finalize=True)

#admin main layout
def create_admin_dashboard_window():
    layout = [
        [sg.Button('Add New Show'),sg.Button("Add New Actor") ,sg.Button('List All Shows'), sg.Button('Logout')]
    ]
    return sg.Window('DataYogi Master', layout, finalize=True)

#user main layout
def create_user_dashboard_window(show_create_list=False):
    layout = [
        [sg.Button('Create List', visible=show_create_list, key='Create List'),
         sg.Button("Add Show to List"),
         sg.Button("Rate Show"),
         sg.Button("View List"),
         sg.Button("View All Shows"),
         sg.Button('Logout')]
    ]
    return sg.Window('DataYogi Padawan', layout, finalize=True)

#user create list layout
def create_user_list_window(list_name, list_description):
    layout = [
        [sg.Text(f"List: {list_name}", font=("Helvetica", 16))],
        [sg.Text(f"Description: {list_description}", font=("Helvetica", 12))],
        [sg.Text('Filter by Label:'),
         sg.Combo(['All', 'Completed', 'Watching', 'Plan to Watch', 'Dropped'], default_value='All', key='filter_label'),
         sg.Button('Apply Filter')],
        [sg.Table(values=[], 
                  headings=['Show ID', 'Show Name', 'Type', 'Genre', 'Year', 'Avg Rating', 'Label', 'User Rating'],
                  key='user_list_table',
                  auto_size_columns=True,
                  enable_click_events=True,  # Enable click events for the table
                  bind_return_key=True)],  # Allow enter key to trigger events
        [sg.Multiline(size=(45, 5), key='comment_input'), sg.Button('Submit Comment')],
        [sg.Button('Refresh List'), sg.Button('Close')]
    ]
    return sg.Window(f"User's Detailed List - {list_name}", layout, finalize=True)
#view all shows layout
def view_all_window():
    layout = [
        [sg.Text(f"BAHŞEGELL", font=("Helvetica", 16))],
        [sg.Table(values=[], 
                  headings=['Show ID', 'Show Name', 'Type', 'Genre', 'Year', 'Avg Rating'],
                  key='shows_table',
                  auto_size_columns=True,
                  enable_click_events=True,  # Enable click events for the table
                  bind_return_key=True)],  # Allow enter key to trigger events
        [sg.Button('Refresh List'), sg.Button('Close')]
    ]
    return sg.Window(f"Deep into movies hah!", layout, finalize=True)

#details layout
def details_window(show_summary, actor_list, comment_text):
    layout = [
        [sg.Text("Summary:")],
        [sg.Multiline(show_summary, size=(45, 5), disabled=True, autoscroll=True)],
        [sg.Text("Actors:")],
        [sg.Multiline(actor_list, size=(45, 2), disabled=True, autoscroll=True)],
        [sg.Text("Comments:")],
        [sg.Multiline(comment_text, size=(45, 10), disabled=True, autoscroll=True)]
    ]
    return sg.Window("Details", layout, finalize=True)

#make sure comment is a table like 
def details_window(show_summary, actor_list, comment_data,is_admin=0):
    # Assuming comment_data is a list of tuples/lists with (username, date, comment_id)

    comment_headers = [ "Comment ID","Username", "Date"]
    comment_table_data = [[comment[0], comment[1], comment[2]] for comment in comment_data]  # Extract required fields
    if is_admin==1:
        layout = [
            [sg.Text("Summary:")],
            [sg.Multiline(show_summary, size=(45, 5), disabled=True, autoscroll=True)],
            [sg.Text("Actors:")],
            [sg.Multiline(actor_list, size=(45, 2), disabled=True, autoscroll=True)],
            [sg.Text("Comments:")],
            [sg.Table(values=comment_table_data, headings=comment_headers, auto_size_columns=True, 
                    display_row_numbers=False,key="delete",enable_click_events=True, num_rows=min(10, len(comment_table_data)))],
            [sg.Button("Close"), sg.Button("Refresh")]
        ]
    else:
       layout = [
            [sg.Text("Summary:")],
            [sg.Multiline(show_summary, size=(45, 5), disabled=True, autoscroll=True)],
            [sg.Text("Actors:")],
            [sg.Multiline(actor_list, size=(45, 2), disabled=True, autoscroll=True)],
            [sg.Text("Comments:")],
            [sg.Table(values=comment_data, headings=comment_headers, key='comment_table', auto_size_columns=True,
            display_row_numbers=False, enable_events=True, num_rows=min(10, len(comment_data))),
            [sg.Button("Close"), sg.Button("Refresh")]]
    ]
    return sg.Window("Details", layout, finalize=True)

#user adds a show to a list layout
def add_show_to_list_window(show_names):
    layout = [
        [sg.Text('Pick a Show'), sg.Combo(show_names, key="show_name")],
        [sg.Text("Label"), sg.Combo(["Completed","Watching","Plan to Watch","Dropped"],key='label')],
        [sg.Button("Add Show"), sg.Button("Cancel")]
    ]
    return sg.Window("Add Show to List", layout, finalize=True)

#user create list layout
def create_list_window():
    layout = [
        [sg.Text('Name'), sg.Input(key='name')],
        [sg.Text('Description'), sg.Input(key='description')],
        [sg.Button('Create'), sg.Button('Cancel')]
    ]
    return sg.Window('Create List', layout, finalize=True)

#user rate show layout
def create_rate_show_window(show_list):
    layout = [
        [sg.Text('Select Show:'), sg.Combo([show for show in show_list], key='selected_show')],
        [sg.Text('Rating:')],
        [sg.Button('★', key='star1', button_color=('yellow', 'white')), 
         sg.Button('☆', key='star2', button_color=('yellow', 'white')), 
         sg.Button('☆', key='star3', button_color=('yellow', 'white')), 
         sg.Button('☆', key='star4', button_color=('yellow', 'white')), 
         sg.Button('☆', key='star5', button_color=('yellow', 'white'))],
        [sg.Button('Submit Rating'), sg.Button('Cancel')]
    ]
    return sg.Window('Rate Show', layout, finalize=True)

#admin adding show layout
def create_add_show_window():
    layout = [
        [sg.Text('Name'), sg.Input(key='name')],
        [sg.Text('Type'), sg.Combo(["Series","Movie"],key='type')],
        [sg.Text('Genre'), sg.Input(key='genre')],
        [sg.Text('Year'), sg.Input(key='year')],
        [sg.Text('Summary'), sg.Input(key='summary')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]
    return sg.Window('Add New Show', layout, finalize=True)

#admin add actor 
def create_add_actor_window(show_names):
    layout = [
        [sg.Text('Name'), sg.Input(key='actor_name')],
        [sg.Text('Surname'), sg.Input(key='actor_surname')],
        [sg.Text('Nationality'), sg.Input(key='actor_nationality')],
        [sg.Text('Birth Date (YYYY-MM-DD)'), sg.Input(key='actor_birth_date')],
        [sg.Text('Gender'), sg.Combo(['Male', 'Female'], key='actor_gender')],
        [sg.Text('Select Show:'), sg.Combo(show_names, key='show_name')],
        [sg.Button('Add Actor'), sg.Button('Cancel')]
    ]
    return sg.Window('Add Actor', layout, finalize=True)

#admin view show layout
def create_view_shows_window():
    layout = [
        [sg.Table(values=[], headings=["Show ID",'Name', 'Type', 'Genre', 'Year', 'Stars', 'Summary'], 
        key='shows_table', auto_size_columns=True, 
        enable_click_events=True)],  # Enable click events
        [sg.Button('Refresh'), sg.Button('Close')]
    ]
    return sg.Window('View Shows', layout, finalize=True)

#sign up window for user with email, gender, password, name, birth_date, surname
def sign_up_window():
    layout = [
        [sg.Text('Name'), sg.Input(key='name')],
        [sg.Text("Surname"), sg.Input(key='surname')],
        [sg.Text("Username"), sg.Input(key="username")],
        [sg.Text("Email"), sg.Input(key='email')],
        [sg.Text("Gender"), sg.Combo(["Male","Female"],key='gender')],
        [sg.Text("Password"), sg.Input(key='password', password_char='g')],
        [sg.Text("Password Again"), sg.Input(key='password_again', password_char='s')],
        [sg.Text("Birth Date (YYYY-MM-DD)"), sg.Input(key='birth_date')],
        
        [sg.Button('Sign Up'), sg.Button('Cancel')]
    ]
    return sg.Window('Sign Up', layout, finalize=True)

#delete comment admin
def delete_comment(comment_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM comments WHERE comment_id = ?", (comment_id,))
        conn.commit()
        sg.popup("Comment deleted successfully.")
    except sqlite3.Error as e:
        sg.popup(f"Error deleting comment: {e}")
    finally:
        conn.close()

#Comment function with email, show_id, comment_id, comment_date and content add to comment table
def comment(email, show_id, comment_id, comment_date, content):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT label FROM add_shows_to_lists WHERE email = ? AND show_id = ?",(email,show_id))
    result = cursor.fetchone()
    if result is not None:
        label = result[0]
        if label not in ['Dropped', 'Completed']:
            sg.popup("You can only comment on shows that are labeled as Dropped or Watched.")
            return False
    else:
        sg.Popup("You can only comment on shows that are in your list.")
        return False
    try:
        cursor.execute("INSERT INTO comments (email, show_id, comment_id, comment_date, content) VALUES (?, ?, ?, ?, ?)",
                       (email, show_id, comment_id, comment_date, content))
        conn.commit()
    except sqlite3.Error as e:      
        sg.popup(f"An error occurred: {e}")
    finally:
        conn.close()
    sg.popup("Comment added successfully!")
    return True

#we need a sign up function
def sign_up(name, email, gender,username, password, password_again, birth_date, surname, db_file=db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM account WHERE email = ?", (email,))
    if cursor.fetchone():
        sg.popup("Email already exists. Please try again.")
        return

    # Check if passwords match
    if password != password_again:
        sg.popup("Passwords do not match. Please try again.")
        return

    # Validate birth date
    try:
        birth_date_obj = dt.datetime.strptime(birth_date, "%Y-%m-%d")
        if birth_date_obj > dt.datetime.now():
            sg.popup("Birth date cannot be in the future yarram. Please try again.")
            return
    except ValueError:
        sg.popup("Invalid birth date format. Please use YYYY-MM-DD.")
        return
    #make sure username is unique
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    if cursor.fetchone():
        sg.popup("Username already exists. Please try again.")
        return
    # Insert data into the database
    try:
        cursor.execute("INSERT INTO account ( email, gender, password, name, birth_date, surname) VALUES (?, ?, ?, ?, ?, ?)",
                       (email, gender, password, name, birth_date,surname)) 
        #also add the email and username to user table
        cursor.execute("INSERT INTO user (email,username) VALUES (?,?)", (email,username))
        conn.commit()
    except sqlite3.Error as e:
        sg.popup(f"An error occurred: {e}")
    finally:
        conn.close()
    sg.popup("User registered successfully!")
    return True
                   

def user_has_list(email):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)


# Function to check Admin Login
def login_admin(email, password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin JOIN account ON admin.email = account.email WHERE admin.email = ? AND password = ?", (email, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to check User Login
def login_user(email, password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user JOIN account ON user.email = account.email WHERE user.email = ? AND password = ?", (email, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def insert_actor(name, surname, nationality, birth_date, gender, show_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        # Insert actor data
        cursor.execute("INSERT INTO actor (name, surname, nationality, birth_date, gender) VALUES (?, ?, ?, ?, ?)", 
                       (name, surname, nationality, birth_date, gender))
        actor_id = cursor.lastrowid  # Get the last inserted row id

        # Get show_id from show_name
        cursor.execute("SELECT show_id FROM show WHERE name = ?", (show_name,))
        show_id = cursor.fetchone()[0]

        # Insert record into play table
        cursor.execute("INSERT INTO play (actor_id, show_id) VALUES (?, ?)", (actor_id, show_id))

        conn.commit()
        sg.popup('Actor added successfully!')
    except sqlite3.Error as e:
        sg.popup(f'Database error: {e}')
    finally:
        conn.close()

# Admin inserts a new show into the database
def insert_show(show_id, name, tipe, genre, year, summary, added_by):
    # Check for empty fields except average_rating
    if not all([name, tipe, genre, year, summary, added_by]):
        sg.popup("Please fill in all fields.")
        return

    # Validate data types and ranges
    try:
        year = int(year)
    except ValueError:
        sg.popup("Invalid year. Please enter a valid year.")
        return

    if not (1895 <= year <= dt.datetime.now().year):
        sg.popup("Invalid year. Please enter a year between 1895 and the current year.")
        return

    if tipe not in ["Series", "Movie"]:
        sg.popup("Invalid type. Please enter 'Series' or 'Movie'.")
        return
   # try:
   #     int(genre)
   #     sg.popup("Invalid genre. Please enter a string.")
   #     return
   # except:
   #     pass
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        query = '''INSERT INTO show(show_id, name, type, genre, year, average_rating, summary, added_by)
                    VALUES(?,?,?,?,?,?,?,?)'''
        cursor.execute(query, (show_id + 1, name, tipe, genre, year, None, summary, added_by))
        conn.commit()
        return True  # Successfully added the show
    except sqlite3.Error as e:
        sg.popup(f'Database error: {e}')  # Display specific error
        return False  # Indicate failure
    finally:
        if conn:
            conn.close()


# User create a list 
def create_list(email, name, description):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the user already has a list
    cursor.execute("SELECT * FROM list WHERE email = ?", (email,))
    if cursor.fetchone():
        sg.popup('You can only create one list per user.')
        conn.close()
        return False

    # Insert the new list
    try:
        addition_date = dt.datetime.now().strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO list (email, list_name, list_description, add_date) VALUES (?, ?, ?, ?)", (email, name, description, addition_date))
        conn.commit()
        sg.popup('List created successfully!')
        return True
    except sqlite3.Error as e:
        sg.popup(f'Database error: {e}')
        return False
    finally:
        conn.close()

# User adds a show to a list
def add_show_to_list(email, show_id, label):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        show_id = int(show_id)
    except ValueError:
        sg.popup('Invalid Show ID. Please enter a valid number.')
        conn.close()
        return
    # Retrieve the user's list name
    cursor.execute("SELECT list_name FROM list WHERE email = ?", (email,))
    result = cursor.fetchone()
    if not result:
        sg.popup('No list found for the user.')
        return

    list_name = result[0]

    # Check if the show exists in the database
    cursor.execute("SELECT * FROM show WHERE show_id = ?", (show_id,))
    if not cursor.fetchone():
        sg.popup('Show not found.')
        return

    # Check if the show is already in the user's list
    cursor.execute("SELECT * FROM add_shows_to_lists WHERE email = ? AND list_name = ? AND show_id = ?", (email, list_name, show_id))
    if cursor.fetchone():
        # Update the label if the show is already in the list
        try:
            cursor.execute("UPDATE add_shows_to_lists SET label = ? WHERE email = ? AND list_name = ? AND show_id = ?", (label, email, list_name, show_id))
            conn.commit()
            sg.popup('Show label updated successfully!')
        except sqlite3.Error as e:
            sg.popup(f'Choose label from the list!')
    else:
        # Insert the show into the list if it's not there already
        try:
            cursor.execute("INSERT INTO add_shows_to_lists (email, list_name, show_id, label) VALUES (?, ?, ?, ?)", (email, list_name, show_id, label))
            conn.commit()
            sg.popup('Show added to list successfully!')
        except sqlite3.Error as e:
            sg.popup(f'Choose label from the list!')
    conn.close()

# User spesific shows
def fetch_user_shows_with_labels(email):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT show.name, add_shows_to_lists.label,show.average_rating FROM show INNER JOIN add_shows_to_lists ON show.show_id = add_shows_to_lists.show_id WHERE add_shows_to_lists.email = ? ", (email,))
    shows_with_labels = cursor.fetchall()
    conn.close()
    return shows_with_labels

# User rates a show labelled correctly
def submit_show_rating(email, show_name, rating, shows_with_labels):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # Fetch show_id for the given show name
    try:
        rating = int(rating) 
    except ValueError:
        sg.popup('Invalid rating. Please enter a valid number between 1 and 5.')
        conn.close()
        return
    cursor.execute("SELECT show_id FROM show WHERE name = ?", (show_name,))
    result = cursor.fetchone()
    if result:
        show_id = result[0]
    else:
        sg.popup('Show not found.')
        return

    # Check if the show is completed or dropped
    if any(show == show_name and label in ['Completed', 'Dropped'] for show, label, _ in shows_with_labels):

        # Check if there is an existing rating
        cursor.execute("SELECT * FROM rate WHERE email = ? AND show_id = ?", (email, show_id))
        if cursor.fetchone():
            # Update the existing rating
            try:
                cursor.execute("UPDATE rate SET rating = ? WHERE email = ? AND show_id = ?", (rating, email, show_id))
                conn.commit()
                sg.popup('Remember you cannot rate more than once. Hence rating updated successfully!')
            except sqlite3.Error as e:
                sg.popup(f'Database error: {e}')
        else:
            # Insert a new rating
            try:
                cursor.execute("INSERT INTO rate (email, show_id, rating) VALUES (?, ?, ?)", (email, show_id, rating))
                conn.commit()
                sg.popup('Rating submitted successfully!')
            except sqlite3.Error as e:
                sg.popup(f'Database error: {e}')
            finally:
                conn.close()

    else:
        sg.popup('You can only rate shows that are completed or dropped. Watch first brother')
        conn.close()


# Getting all the shows from the database
def get_all_shows():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT show_id,name, type, genre, year, average_rating, summary FROM show")
    shows = cursor.fetchall()
    conn.close()
    return [list(show) for show in shows]  # Convert each tuple to a list

#get show_id by show_name
def get_show_id_by_name(show_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT show_id FROM show WHERE name = ?", (show_name,))
    result = cursor.fetchone()
    conn.close()
    try:
        show_id = result[0]
    except TypeError:
        show_id = None
    return show_id

def get_show_comments(show_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT content, email FROM comment WHERE show_id = ?", (show_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

#get details of show
def get_show_details(show_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # Query to fetch show summary and actor names
    query = """
        SELECT show.summary, GROUP_CONCAT(actor.name || ' ' || actor.surname, ', ') as actors
        FROM show
        LEFT JOIN play ON show.show_id = play.show_id
        LEFT JOIN actor ON play.actor_id = actor.actor_id
        WHERE show.show_id = ?
        GROUP BY show.show_id
    """
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()
    conn.close()
    return result  # Returns a tuple like ('This is the summary.', 'Actor1 Name, Actor2 Name')

# Fetch the list of a user by user email
def get_detailed_user_list(email):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQL query to fetch the required information along with the rating count
    query = """
    SELECT 
        s.show_id, s.name, s.type, s.genre, s.year, 
        IFNULL(avg_rating.avg, 'Not Rated') AS Avg_Rating, 
        IFNULL(avg_rating.count, 0) AS Rating_Count,
        ar.label, r.rating 
    FROM 
        add_shows_to_lists ar
    LEFT JOIN 
        show s ON ar.show_id = s.show_id
    LEFT JOIN 
        rate r ON ar.show_id = r.show_id AND ar.email = r.email
    LEFT JOIN 
        (SELECT show_id, AVG(rating) AS avg, COUNT(rating) AS count FROM rate GROUP BY show_id) avg_rating 
        ON s.show_id = avg_rating.show_id
    WHERE 
        ar.email = ?
    """

    cursor.execute(query, (email,))
    user_list = cursor.fetchall()
    conn.close()

    # Convert the fetched data into a list of dictionaries for easier handling
    detailed_list = []
    for item in user_list:
        avg_rating_display = f"{item[5]} ({item[6]} ratings)" if item[5] != 'Not Rated' else 'Not Rated'
        user_rating_display = item[8] if item[8] is not None else 'Not Rated'
        show_details = {
            'Show ID': item[0],
            'Show Name': item[1],
            'Type': item[2],
            'Genre': item[3],
            'Year': item[4],
            'Average Rating': avg_rating_display,
            'Label': item[7],
            'User Rating': user_rating_display,
            'More Details': 'Click for More'  # Add "Click for More" string to each row
        }
        detailed_list.append(show_details)

    return detailed_list



def main():
    login_window = create_login_window()
    admin_window = None
    add_show_window = None
    user_window = None
    view_shows_window = None
    list_window = None
    logged_in_admin = None
    logged_in_user = None
    rate_show_window = None
    user_list_window = None
    list_show_window = None 
    add_actor_window = None
    signup_window = None
    user_rating = 0 
    first_time_accessing_list = True
    admin_in = 0
    user_in = 0
    det_window = None
    


    

    while True:
        window, event, values = sg.read_all_windows()

        if event == 'Logout':
            if admin_window:
                admin_window.close()
                admin_window = None
            if user_window:
                user_window.close()
                user_window = None
            logged_in_admin = None
            logged_in_user = None
            login_window = create_login_window()

        if event == 'Cancel':
            if window == login_window:
                break  # Exit the app if 'Cancel' is clicked in the login window
            else:
                window.close()  # Close the current window and continue the loop
                if window == admin_window or window == user_window:
                    login_window.un_hide()  # Un-hide the login window if an admin or user window is closed
        elif event == sg.WIN_CLOSED:
            if window == login_window:
                break  # Break the loop and exit the app if the login window is closed
            else:
                window.close()  # Close other windows and continue the loop

        #login dashboard
        if window == login_window:
            if event == 'Login as Admin':
                if login_admin(values['email'], values['password']):
                    sg.popup("Welcome Master!")
                    login_window.hide()
                    admin_window = create_admin_dashboard_window()
                    logged_in_admin = values['email']
                    admin_in = 1
                else:
                    sg.popup("Login Failed")

            elif event == 'Login as User':
                if login_user(values['email'], values['password']):
                    first_time_accessing_list = True
                    sg.popup("Welcome to DataYogiFilmCehennemi!")
                    login_window.hide()
                    # Check if the user already has a list
                    has_list = user_has_list(values['email'])
                    user_window = create_user_dashboard_window(show_create_list=not has_list)
                    logged_in_user = values['email']
                else:
                    sg.popup("Login Failed")
            
            elif event == 'Sign Up':
                signup_window = sign_up_window()
                login_window.hide()
                signup_window.un_hide()
                signup_window.bring_to_front()


            elif event == sg.WIN_CLOSED or event == 'Cancel':  # Handle window close and Cancel button
                if window == login_window:
                    break  # Only break the loop if the login window is closed
                else:
                    window.close()  # Close other windows without breaking the loop

        elif window == signup_window:
            if event == 'Sign Up':
                username = values["username"]
                name = values['name']
                surname = values['surname']
                email = values['email']
                password = values['password']
                password_again = values["password_again"]
                birth_date = values['birth_date']
                gender = values['gender']
                if sign_up(name, email, gender,username, password, password_again, birth_date, surname):
                        signup_window.close()
                        signup_window = None
                        login_window.un_hide()
                else:
                        sg.popup("Signup Failed")


            elif event == 'Cancel':
                signup_window.close()
                signup_window = None
                login_window.un_hide()
        #admin dashboard
        elif window == admin_window:
                if event == 'Add New Show':
                    add_show_window = create_add_show_window()
                    admin_window.hide()
                    add_show_window.un_hide()
                    add_show_window.bring_to_front()

                if event == 'Add New Actor':
                    show_names = [show[1] for show in get_all_shows()]
                    add_actor_window = create_add_actor_window(show_names)
                    admin_window.hide()
                    add_actor_window.un_hide()
                    add_actor_window.bring_to_front()
         
                elif event == 'List All Shows':
                    shows = get_all_shows()
                    view_shows_window =  view_all_window()
                    view_shows_window['shows_table'].update(shows)
                    view_shows_window.un_hide()
                    admin_window.hide()
                    view_shows_window.bring_to_front()
                    

                elif event == 'Logout':
                    login_window.un_hide()
                    admin_window.close()
                    login_window = None
                    admin_window = None
                    logged_in_admin = None
        #add actor layout
        elif window == add_actor_window:
            if event == 'Add Actor':
                name = values['actor_name']
                surname = values['actor_surname']
                nationality = values['actor_nationality']
                birth_date = values['actor_birth_date']
                gender = values['actor_gender']
                show_name = values['show_name']
                if all([name, surname, nationality, birth_date, gender, show_name]):
                    insert_actor(name, surname, nationality, birth_date, gender, show_name)
                else:
                    sg.popup("Please fill in all fields.")

            elif event == 'Cancel':
                add_actor_window.close()
                add_actor_window = None
                admin_window.un_hide()
                admin_window.refresh()
                admin_window.bring_to_front()

        #add show window for admins
        elif window == add_show_window:
            if event == "Submit":
                    conn = sqlite3.connect('datayogi_implementation_stage.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT show_id FROM show ORDER BY show_id DESC LIMIT 1")
                    result = cursor.fetchone()
                    show_id = result[0] if result else 0  # Start from 1 if there are no shows yet
                    name = values["name"]
                    tipe = values['type']
                    genre = values['genre']
                    year = values['year']
                    summary = values['summary']

                    # Call the revised insert_show function
                    success = insert_show(show_id, name, tipe, genre, year, summary, logged_in_admin)
                    if success:
                        sg.popup('Show added successfully!', title='Success')
                    else:
                        sg.popup('Failed to add the show. Please try again.', title='Error')
            elif event == "Cancel":
                add_show_window.close()
                add_show_window = None
                #go back to admin dashboard
                admin_window.un_hide()
                admin_window.refresh()
                admin_window.bring_to_front()
            else:
                sg.popup("Error")

        #view show window for everyone 
        elif window == view_shows_window:
                if event == 'Close':
                    view_shows_window.close()
                    view_shows_window = None  # Reset the variable to None after closing
                    try:
                        user_window.un_hide()
                        user_window.refresh()
                        user_window.bring_to_front()
                    except:
                        admin_window.un_hide()
                        admin_window.refresh()
                        admin_window.bring_to_front()
                        
                
                if event == 'shows_table':  # Assuming 'shows_table' is the key for your table
                    try:
                        selected_row_index = values['shows_table'][0]  # Get the first selected row index
                        selected_show_id = shows[selected_row_index][0]  # Assuming the first column is the show ID
                
                        # Fetch additional details for the selected show
                        conn = sqlite3.connect(db_file)
                        cursor = conn.cursor()
                        # Fetch show summary
                        cursor.execute("SELECT summary FROM show WHERE show_id = ?", (selected_show_id,))
                        try:
                            show_summary = cursor.fetchone()[0]
                        except:
                            show_summary = "No summary"
                        
                        # Fetch actors
                        cursor.execute("SELECT name, surname FROM actor INNER JOIN play ON actor.actor_id = play.actor_id WHERE show_id = ?", (selected_show_id,))
                        actors = cursor.fetchall()
                        actor_list = ', '.join([f"{name} {surname}" for name, surname in actors]) if actors else "No actors listed."
                        # Fetch comments
                        cursor.execute("SELECT comment_id,username, content FROM comments INNER JOIN user ON comments.email = user.email WHERE show_id = ?", (selected_show_id,))
                        comments = cursor.fetchall()
                        comment_table_data = [[comment_id, username, content] for comment_id, username, content in comments]

                        # Open the details window with the latest comments data
                        det_window = details_window(show_summary, actor_list, comment_table_data, is_admin=admin_in)
                        det_window.un_hide()
                        sg.popup("You can click on the comment to delete biaaaç")

                    except:
                        pass
                            
                   
                elif event == 'Refresh':
                                shows_data = get_all_shows()
                                if view_shows_window:  # Check if the window is still open
                                    view_shows_window['shows_table'].update(values=shows_data)
        
        elif window == det_window:
            if event == 'Close':
                det_window.close()
                det_window = None
                if user_window:
                    user_window.un_hide()
                    user_window.refresh()
                    user_window.bring_to_front()
                else:
                    admin_window.un_hide()
                    admin_window.refresh()
                    admin_window.bring_to_front()

            elif 'delete' in event:
                     
                    selected_row_index = values["delete"][0]  # Get the index of the selected row
                    print("Debug1:",selected_row_index)
                    selected_comment_id = comment_table_data[selected_row_index][0]  # Extract the comment ID
                    print("Debug2:",selected_comment_id)
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM comments WHERE comment_id = ?", (selected_comment_id,))
                    conn.commit()
                    # Confirmation dialog
                    if sg.popup_yes_no("Are you sure you want to delete this comment?") == 'Yes':
                        delete_comment(selected_comment_id)
                            # Refresh the comments display here (re-fetch comments and update the table)
            elif event == "Refresh":
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT comment_id,username, content FROM comments INNER JOIN user ON comments.email = user.email WHERE show_id = ?", (selected_show_id,))
                comments = cursor.fetchall()
                comment_table_data = [[comment_id, username, content] for comment_id, username, content in comments]
                sg.popup("Comments refreshed.")
            
            else:
                sg.popup("Error")
        
        #user dashboard
        elif window == user_window:
            if event == 'Create List':
                list_window = create_list_window()
                if list_window:  # Check if the window was created successfully
                    user_window.hide()
                    list_window.un_hide()
                    list_window.bring_to_front()
                else:
                    print("Failed to create list window")

            elif event == "Add Show to List":
                show_names = [name[1] for name in get_all_shows()]
                list_show_window = add_show_to_list_window(show_names)
                user_window.hide()
                list_show_window.un_hide()
                list_show_window.bring_to_front()

            elif event == "Rate Show":
                shows_with_labels = fetch_user_shows_with_labels(logged_in_user)
                rate_show_window = create_rate_show_window([show[0] for show in shows_with_labels])
                user_window.hide()
                rate_show_window.un_hide()
                rate_show_window.bring_to_front()

            elif event == 'View List':
                if first_time_accessing_list:
                    sg.popup("Tip: Click on any movie in the list to view more details ;)", title="Information")
                    first_time_accessing_list = False
                # Fetch the list name and description for the logged-in user
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT list_name, list_description FROM list WHERE email = ?", (logged_in_user,))
                list_info = cursor.fetchone()
                conn.close()
                if list_info:
                    list_name, list_description = list_info
                    user_list_window = create_user_list_window(list_name, list_description)
                    user_list_data = get_detailed_user_list(logged_in_user)
                    user_list_window['user_list_table'].update(values=[[d['Show ID'], d['Show Name'], d['Type'], d['Genre'], d['Year'], d['Average Rating'], d['Label'], d['User Rating']] for d in user_list_data])
                    user_window.hide()
                    user_list_window.un_hide()
                    user_list_window.bring_to_front()
                else:
                    sg.popup("No list found for the user.")

            elif event == "View All Shows":
                shows = get_all_shows()
                view_shows_window = view_all_window()
                view_shows_window['shows_table'].update(shows)
                view_shows_window.un_hide()
                user_window.hide()
                view_shows_window.bring_to_front()

            elif event == 'Logout':
                login_window.un_hide()
                user_window.close()
                user_window = None
                logged_in_user = None
                login_window.refresh()
                login_window.bring_to_front()
        #user sees his list
        elif window == user_list_window:
            if event == 'Apply Filter':
                label_filter = values['filter_label']  # The key 'filter_label' should match your Combo element's key
                filtered_data = []

                for row in user_list_data:  # 'user_list_data' should be a list of dictionaries representing the user's list items
                    if label_filter == 'All' or row['Label'] == label_filter:
                        filtered_data.append(row)

                # Update the table with filtered data
                user_list_window['user_list_table'].update(values=[[d['Show ID'], d['Show Name'], d['Type'], d['Genre'], d['Year'], d['Average Rating'], d['Label'], d['User Rating']] for d in filtered_data])
                
            if event == 'user_list_table':               
                try:
                    row = values['user_list_table'][0]  # Get the row index
                    show_id = user_list_data[row]['Show ID']  # Get the show ID from the selected row
                    # Fetch show details and display in a popup
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT summary FROM show WHERE show_id = ?", (show_id,))
                    show_summary = cursor.fetchone()[0]
                    # Fetch actors for the show
                    cursor.execute("SELECT name, surname FROM actor INNER JOIN play ON actor.actor_id = play.actor_id WHERE show_id = ?", (show_id,))
                    actors = cursor.fetchall()
                    actor_list = ', '.join([f"{name} {surname}" for name, surname in actors])
                    # Fetch comments
                    cursor.execute("SELECT comment_id,username, content FROM comments INNER JOIN user ON comments.email = user.email WHERE show_id = ?", (show_id,))
                    comments = cursor.fetchall()
                    comment_text = ([comment_id,username,content] for comment_id, username, content in comments) if comments else "No comments yet."
                        
                    details_window(show_summary,actor_list,comment_text).un_hide
            
                except IndexError:
                        pass  # No row was selected
                finally:
                    if conn:
                        conn.close()
            elif event == 'Refresh List':
                user_list_data = get_detailed_user_list(logged_in_user)
                user_list_window['user_list_table'].update(values=[[d['Show ID'], d['Show Name'], d['Type'], d['Genre'], d['Year'], d['Average Rating'], d['Label'], d['User Rating']] for d in user_list_data])
            
            elif event == 'Submit Comment':
                selected_rows = values['user_list_table']  # This is likely a list of selected row indices
                if selected_rows:  # Check if at least one row is selected
                    selected_row_index = selected_rows[0]  # Get the index of the first selected row
                    content = values['comment_input']  # Get the comment text
                    show_id = user_list_data[selected_row_index]['Show ID']  # Retrieve show ID from the first selected row
                    email = logged_in_user
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()  # Create a cursor object to execute SQL queries
                    if cursor.execute("SELECT * FROM comments").fetchone():  # Check if there are any comments in the table
                        comment_id = cursor.execute("SELECT MAX(comment_id) FROM comments").fetchone()[0] + 1  # Generate a unique comment ID
                        conn.close()
                    else:
                        comment_id = 1
                    comment_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time as a string
                    # Call the comment function with all required parameters
                    comment(email, show_id, comment_id, comment_date, content)
                else:
                    sg.popup("Please select a show to comment on.")


            elif event == 'Close':
                user_list_window.close()
                user_window.un_hide()
                user_window.refresh()

        #user creates list
        elif window == list_window:      
            if event == 'Create':
                name = values['name']
                description = values['description']

                if not name.strip():
                    sg.popup("Please enter a name for the list.")
                elif not description.strip():
                    sg.popup("Please enter a description for the list.")
                else:
                    success = create_list(logged_in_user, name, description)
                    if success:
                        list_window.close()
                        list_window = None
                        user_window.un_hide()
                        user_window.refresh()
                        user_window.bring_to_front()   
                        user_window['Create List'].update(visible=False)
            elif event == 'Cancel':
                list_window.close()
                list_window = None  # Reset the variable to None after closing
                user_window.un_hide()
                user_window.refresh()
                user_window.bring_to_front()

        #user add shows to list
        elif window == list_show_window:
            if event == 'Add Show':
                    email = logged_in_user
                    show_id = get_show_id_by_name(values['show_name'])
                    label = values['label']
                    try:
                        add_show_to_list(email ,show_id, label)
                    except:
                        sg.popup("Invalid Show.")     
                    shows_with_labels = fetch_user_shows_with_labels(logged_in_user)
                    list_show_window.close()
                    list_show_window = None  # Reset the variable to None after closing
                    user_window.un_hide()
                    user_window.refresh()
                    user_window.bring_to_front()

            elif event == 'Cancel':
                list_show_window.close()
                list_show_window = None  # Reset the variable to None after closing
                user_window.un_hide()
                user_window.refresh()
                user_window.bring_to_front()
        #user rates show
        elif window == rate_show_window:
            if event in ['star1', 'star2', 'star3', 'star4', 'star5']:
                user_rating = int(event[-1])  # Correctly retrieve the rating number
                for i in range(1, 6):
                    window[f'star{i}'].update('★' if i <= user_rating else '☆')
            
            elif event == 'Submit Rating':
                selected_show = values['selected_show']
                # Use the user_rating for submission
                submit_show_rating(logged_in_user, selected_show, user_rating, shows_with_labels)
                rate_show_window.close()
                user_window.un_hide()
                user_window.refresh()
                user_window.bring_to_front()
                rate_show_window = None

            elif event == 'Cancel':
                rate_show_window.close()
                rate_show_window = None
                user_window.un_hide()
                user_window.refresh()
                user_window.bring_to_front()
    for win in [login_window, admin_window, user_window, list_window, rate_show_window, view_shows_window]:
        if win:
            win.close()

main()