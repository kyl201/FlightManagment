import sqlite3

#Create tables 
def create_table():
    db = sqlite3.connect("flights.db")
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Country(
        country_code CHAR(2) UNIQUE NOT NULL PRIMARY KEY,
        country_name VARCHAR(50) UNIQUE NOT NULL 
        )
    ''')
    print("Country table created successfully.")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Airport(
            airport_code CHAR(3) PRIMARY KEY,  
            airport_name  TEXT  NOT NULL,
            city VARCHAR(50) NOT NULL,
            country_code CHAR(2) NOT NULL,
            FOREIGN KEY (country_code ) REFERENCES Country(country_code)
            ON DELETE CASCADE
        )
    ''')
    print("Airport table created successfully.")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FlightStatus (
            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            status CHAR(10) UNIQUE NOT NULL
        )
    ''')
    print("FlightStatus table created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PilotRank  (
            rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank_name VARCHAR(20) UNIQUE NOT NULL
        )
    ''')
    print("PilotRank table created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Route  (
            route_id  INTEGER PRIMARY KEY AUTOINCREMENT ,
            origin_code CHAR(3) NOT NULL,
            destination_code CHAR(3) NOT NULL,
            distance_miles FLOAT NOT NULL,
            duration_minutes INTEGER NOT NULL, 
            UNIQUE (origin_code,destination_code),
            FOREIGN KEY (origin_code ) REFERENCES Airport(airport_code),
            FOREIGN KEY (destination_code) REFERENCES Airport(airport_code)
        )
    ''')
    print("Route table created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pilot  (
            pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            license_no CHAR(10) UNIQUE NOT NULL,
            licence_expiry DATE NOT NULL,
            rank_id INTEGER NOT NULL,
            FOREIGN KEY (rank_id) REFERENCES PilotRank(rank_id)
        )
    ''')
    print("Pilot table created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Flight (
        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_no TEXT GENERATED ALWAYS AS ( 'FL' || printf('%03d', flight_id) )   STORED  UNIQUE,
        route_id INTEGER NOT NULL,
        scheduled_departure DATETIME NOT NULL,
        status_id INTEGER DEFAULT 1, 
        FOREIGN KEY (route_id) REFERENCES Route(route_id)
        ON DELETE CASCADE,
        FOREIGN KEY (status_id) REFERENCES FlightStatus(status_id)
        )
    ''')
    print("Flight table created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PilotAssignment (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id  INTEGER NOT NULL,
        pilot_id INTEGER NOT NULL,            
        FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
        FOREIGN KEY (pilot_id) REFERENCES Pilot(pilot_id) 
        )
    ''')
    print("PilotAssignment table created successfully.")

