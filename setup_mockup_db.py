# File: setup-mockup-db.py
# Date: 3/12/2019 (somewhere around there it was first created)
# Purpose: generate a mockup database with SQLLite

import sqlite3, copy, datetime

# Needed to generate student data
names = [
        "John Glover",
        "Ruth Geraldson",
        "Ron Windler",
        "Everet Stinson",
        "Paula Field",
        "Tiberias Rayhen",
        "Kaylin Rhen",
        "Brandan Slater",
        "Deric Chandler",
        "Ryan Jonathan",
        "Rita Slovac",
        "Irene Novac",
        "Paul Photon",
        "Ira Halep",
        "Guy Gregory",
        "Simona Crison",
        "Hayles Eren",
        "Guy Wilson",
        "Daniel Wilson",
        "Jacob Paulson",
        "Aurel Elric",
        "Ada Green",
        "Ryan Ghan",
        "AJ Breyer-Mugnhen",
        "Emily Manson",
        "Karen Elric",
        "Andy Teran",
        "Leeroy McClain",
        "Erin Wells",
        "Paulson Brown",
        "Charlier Christopher",
        "Adam Polson",
        "Lee Henderson",
        "Adam Nguyen",
        "Karen Barber",
        "Deric Montag",
        "LeAnn Bronson",
        "Ruth Farrari"
]

# A model review to base the midterm and final review off of
example_review = {
        "time": 1,
        #"session_id": 2,
        "tech_mastery": 1,
        "work_ethic": 2,
        "communication": 3,
        "cooperation": 4,
        "initiative": 5,
        "team_focus": 1,
        "contribution": 2,
        "leadership": 2,
        "organization": 3,
        "delegation": 3,
        "points": 4,
        "strengths": ("Everything. You are good at everything. There isn't a "
                      "single problem. Nope."),
        "weaknesses": ("So there are a couple of things. One being your sense" 
                       " of humor. Another being your inability and lack of "
                       "willingness to yodel loudly in public places for no "
                       "given reason."),
        "traits_to_work_on": ("Yodeling, Kool-Aid style, wall destroying "
                              "runs, and your decisions to repeatedly press "
                              "the button for the floor you want to go to "
                              "when on the elevator--it doesn't make it go "
                              "faster."),
        "proud_of_accomplishment": "yes?"
}

def generate_student_data():
    id_num = 1
    team_num = 1
    student_data = []
    for name in names:
        # Generate email address
        split_names = name.split(' ')
        email_address = split_names[0] + "." + split_names[1] + ".notreal@pdx.edu"

        # Get student id
        student_id = id_num
        id_num = id_num + 1

        # Get team number
        #team_number = team_num
        #if (team_num == 6):
        #    team_num = 1
        #else:
        #    team_num = team_num + 1

        # Add Data To List
        student_data.append({"name": name, "email_address": email_address, "id": student_id})#, team_number))

        # Debug
        #print((name, email_address, student_id, team_number))
        #print(teams["Team " + str(team_number)])

    return student_data

def generate_tables(cursor):
    # Create capstone session table and insert a row
    cursor.execute(('CREATE TABLE capstone_session( '
                       'id INTEGER PRIMARY KEY, '
                       'start_term VARCHAR(10), '
                       'start_year INTEGER, '
                       'end_term VARCHAR(10), '
                       'end_year INTEGER );'))

    # Create teams table and insert some rows
    cursor.execute(('CREATE TABLE teams( '
                       'id INTEGER PRIMARY KEY, '
                       'session_id INTEGER REFERENCES capstone_session(id), '
                       'name VARCHAR(128) );'))

    # Create Students Table
    cursor.execute(('CREATE TABLE students( '
                       'id INTEGER, '
                       'tid INTEGER REFERENCES teams(id), '
                       'session_id INTEGER REFERENCES capstone_session(id), '
                       'name VARCHAR(128), '
                       'midterm_done BOOLEAN, '
                       'final_done BOOLEAN, '
                       'PRIMARY KEY (id, session_id) );'))

    # Create Team Members table
    cursor.execute(('CREATE TABLE team_members( '
                       'tid INTEGER REFERENCES teams(id), '
                       'sid INTEGER REFERENCES students(id), '
                       'session_id INTEGER REFERENCES capstone_session(id), '
                       'PRIMARY KEY (tid, sid, session_id) );'))

    # Create Reports table
    cursor.execute(('CREATE TABLE reports('
                       'time TIME, '
                       'session_id INTEGER REFERENCES capstone_session(id), '
                       'reporting INTEGER REFERENCES students(id), '
                       'tid INTEGER REFERENCES teams(id), '
                       'report_for INTEGER REFERENCES students(id), '
                       'tech_mastery INTEGER, '
                       'work_ethic INTEGER, '
                       'communication INTEGER, '
                       'cooperation INTEGER, '
                       'initiative INTEGER, '
                       'team_focus INTEGER, '
                       'contribution INTEGER, '
                       'leadership INTEGER, '
                       'organization INTEGER, '
                       'delegation INTEGER, '
                       'points INTEGER, '
                       'strengths VARCHAR(4096), '
                       'weaknesses VARCHAR(4096), '
                       'traits_to_work_on VARCHAR(4096), '
                       'what_you_learned VARCHAR(4096), '
                       'proud_of_accomplishment VARCHAR(4096), '
                       'is_final BOOLEAN, '
                       'PRIMARY KEY (reporting, tid, report_for, is_final));'))

    # Create removed students table
    cursor.execute(('CREATE TABLE removed_students( '
                       'id INTEGER, '
                       'tid INTEGER REFERENCES teams(id), '
                       'session_id INTEGER REFERENCES capstone_session(id), '
                       'name VARCHAR(128), '
                       'midterm_done BOOLEAN, '
                       'final_done BOOLEAN, '
                       'session_removed INTEGER REFERENCES capstone_session(id), '
                       'PRIMARY KEY (id, session_id) );'))

def submit_review(cursor, student_id, session_id, review):
    # Put midterm review into database
    cursor.execute(('INSERT INTO reports '
                    'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'),
                       (datetime.datetime.now(),
                        session_id,
                        review["reporting"], 
                        review["tid"], 
                        review["report_for"], 
                        review["tech_mastery"], 
                        review["work_ethic"], 
                        review["communication"], 
                        review["cooperation"], 
                        review["initiative"], 
                        review["team_focus"], 
                        review["contribution"], 
                        review["leadership"], 
                        review["organization"], 
                        review["delegation"], 
                        review["points"], 
                        review["strengths"], 
                        review["weaknesses"], 
                        review["traits_to_work_on"], 
                        review["what_you_learned"], 
                        review["proud_of_accomplishment"], 
                        review["is_final"]))

def fill_tables_with_data(cursor, student_data, num_sessions, num_teams):
    for session_id in range(num_sessions):
        # Put new session entry into the database
        cursor.execute('INSERT INTO capstone_session VALUES(?,?,?,?,?)',
                       (session_id, "winter", 2019 + session_id, "spring", 2019 + session_id))

        # Put new team entry into the database
        for team_id in range(num_teams):
            cursor.execute('INSERT INTO teams VALUES(?,?,?)', (team_id + (session_id * num_teams), session_id, "Team " + str(team_id + (session_id * num_teams) + 1)))

        # Put data into the students, teams, team members, and reports tables
        for student in student_data:
            student_id = student["id"] + (len(student_data) * session_id)
            team_id = student["id"] % num_teams + (num_teams * session_id)
            
            # Add student to the students table
            cursor.execute('INSERT INTO students VALUES(?,?,?,?,?,?)',
                           (student_id, team_id, session_id, student["name"], False, False))
    
            # Add student to the team members table
            cursor.execute('INSERT INTO team_members VALUES(?,?,?)',
                           (team_id, student_id, session_id))

            # Create mock midterm report templates from example report
            midterm = copy.deepcopy(example_review)
            midterm["reporting"] = student_id
            midterm["tid"] = team_id
            midterm["is_final"] = False
            midterm["what_you_learned"] = ""

            # Create mock final report template from midterm report template
            final = copy.deepcopy(midterm)
            final["is_final"] = True

            # Generate a report for each member of the student's team and put it
            # into the database
            for team_member_id in range(num_teams):
                # Get the id of the student the reports are for
                target_student = session_id * len(student_data) + (team_member_id * num_teams)
                
                # Create midterm report
                new_midterm = copy.deepcopy(midterm)
                new_midterm["report_for"] = target_student

                # Create final
                new_final = copy.deepcopy(final)
                new_final["report_for"] = target_student
                if (team_member_id == student_id):
                    new_final["what you learned"] = "How to make a web app. Yah!"

                # Debug
                #print (new_midterm)
                #print (new_final)
                #print()

                # Put midterm review into database
                submit_review(cursor, student_id, session_id, new_midterm)
                cursor.execute(('UPDATE students SET midterm_done = ? WHERE id = ? '
                                 'AND session_id = ?'), (True, student_id, session_id))
    
                # Put final review into database
                submit_review(cursor, student_id, session_id, new_final)
                cursor.execute(('UPDATE students SET final_done = ? WHERE id = ? '
                                 'AND session_id = ?'), (True, student_id, session_id))

def main():
    # Part 1: Create database and add tables
    connection = sqlite3.connect('mockup-database.db')
    cursor = connection.cursor()
    generate_tables(cursor)

    # Part 2: Add student and student data to database
    fill_tables_with_data(cursor, generate_student_data(), 3, 6)

    # Commit database changes and close the connection to the database
    connection.commit()
    connection.close()

# Run Everything
#main()
