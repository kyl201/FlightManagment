import sqlite3

#Insert sample data in the tables
def sample_data():
    db = sqlite3.connect("flights.db")
    cursor = db.cursor()

    # Insert sample data into Country table
    cursor.execute('''
        INSERT OR IGNORE INTO Country (country_code, country_name)
        VALUES  ('GB','United Kingdom'),('US','United States'),('TH','Thailand'),
                ('FR','France'),('IT','Italy'),('CA','Canada'),
                ('DE','Germany'),('ZA','South Africa'),('ES','Spain')
    ''')
    print("Country data added.")

    cursor.execute('''
        INSERT OR IGNORE INTO PilotRank (rank_name)
        VALUES  ('Captain'),('First Officer')
    ''')
    print("PilotRank data added.")

    
    # Insert sample data into Airport table
    cursor.execute('''
        INSERT OR IGNORE INTO Airport (airport_code, airport_name, city, country_code)
        VALUES  ('LHR', 'Heathrow Airport', 'London', 'GB'),
                ('JFK', 'John F. Kennedy International Airport', 'New York', 'US'),
                ('BKK', 'Suvarnabhumi Airport', 'Bangkok', 'TH'),
                ('CDG', 'Charles de Gaulle Airport', 'Paris', 'FR'),
                ('FCO', 'Leonardo da Vinci International Airport', 'Rome', 'IT'),
                ('YYZ', 'Toronto Pearson International Airport', 'Toronto', 'CA'),
                ('FRA', 'Frankfurt Airport', 'Frankfurt', 'DE'),
                ('JNB', 'O.R. Tambo International Airport', 'Johannesburg', 'ZA'),
                ('MAD', 'Adolfo Suárez Madrid–Barajas Airport', 'Madrid', 'ES')
    ''')
    print("Airport data added.")

    
    # Insert sample data into FlightStatus table
    cursor.execute('''
        INSERT OR IGNORE INTO FlightStatus (status)
        VALUES  ('Scheduled'),('Delayed'),('Boarding'),
        ('Departed'),('Landed'),('Arrived'),('Cancelled');
    ''')
    print("FlightStatus data added.")
    

    # Insert sample data into Route table
    cursor.execute('''
        INSERT OR IGNORE INTO Route (origin_code, destination_code, distance_miles,duration_minutes)
        VALUES  ('LHR', 'JFK', 3451.4, 444), ('LHR', 'BKK', 5958.2, 693), 
                ('LHR', 'CDG', 216.1, 81), ('LHR', 'FCO', 898.4, 155),
                ('LHR', 'YYZ', 3556.4, 479), ('LHR', 'FRA', 407.1, 100), 
                ('LHR', 'JNB', 5620.4, 662), ('LHR', 'MAD',  772.6, 145 );
    ''')
    print("Route data added.")

    # Insert sample data into Pilot table
    cursor.execute('''
        INSERT OR IGNORE INTO Pilot (first_name, last_name, license_no, licence_expiry, rank_id)
        VALUES  ('Adam', 'Smith', 'A0123456', '2028-05-18', 1),
                ('Alison', 'Thompson', 'A0123457', '2028-01-18', 1),
                ('Christopher', 'Hodges', 'A0123458', '2028-03-20', 1),
                ('Karen', 'Hilll', 'A0123459', '2028-01-11', 1),
                ('Chloe', 'Ogden', 'A0123460', '2028-07-11', 1),
                ('Sean', 'Reid', 'A0123461', '2028-06-01', 1),
                ('Naomi', 'Scott', 'A0123462', '2026-09-01', 1),
                ('Olivia', 'Blake', 'A0123463', '2025-08-01', 1),
                ('Nicholas', 'Gary', 'A0123464', '2029-08-01', 1),
                ('Tom', 'Hudson', 'A0123465', '2025-12-01', 1),
                ('Kelly', 'King', 'A0123466', '2026-04-01', 1),
                ('Taylor', 'Lewis', 'A0123467', '2027-05-01', 2),
                ('Martin', 'Young', 'A0123468', '2026-03-01', 2),
                (' Max', 'Wright', 'A0123469', '2028-08-11', 2);
    ''')
    print("Pilot data added.")

    cursor.execute('''
        INSERT OR IGNORE INTO Flight (route_id, scheduled_departure)
        VALUES  (1, '2025-08-26 10:55:00'),
                (2, '2025-08-28 18:00:00' ),
                (3, '2025-08-28 22:15:00'),
                (4, '2025-08-29 20:40:00'),
                (5, '2025-08-29 21:25:00'),
                (1, '2025-08-30 21:25:00'),   
                (2, '2025-08-31 12:50:00'),
                (2, '2025-09-01 17:30:00'),
                (3, '2025-09-01 20:00:00'),
                (4, '2025-09-02 12:50:00'),
                (5, '2025-09-03 16:50:00');
    ''')
    print("Flights data added.")
 
    cursor.execute('''
        INSERT OR IGNORE INTO PilotAssignment (flight_id, pilot_id)
        VALUES  (1 ,1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5 ,1),
                (6, 5);
    ''')
    print("PilotAssignment data added.")

    # Commit the changes and close the connection
    db.commit()
    db.close()
if __name__ == "__main__":
    seed_data()
    print("Database seed data added.")
 