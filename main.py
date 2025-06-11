import sqlite3
import schema
import sample
import re
from datetime import date, datetime
from tabulate import tabulate


# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("flights.db")
      self.cur = self.conn.cursor()
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  def get_connection(self):
    self.conn = sqlite3.connect("flights.db")
    self.cur = self.conn.cursor()
  
  # This method retrive all the tables name in flights.db and then deletes them.
  def delete_all_tables(self):
    try:  
      self.get_connection()
      self.cur.execute("""SELECT name 
                       FROM sqlite_master  
                       WHERE type='table'
                       AND name NOT LIKE 'sqlite_%';
                       """)
      table_names = [row[0] for row in self.cur.fetchall()]
      if not table_names:
         print("There are no existing table.")
      else: 
          for table in table_names:
            self.cur.execute(f'DROP TABLE IF EXISTS "{table}";')
            print(f"{table} deleted from flights.db")
      print('All tables form flight.db have been deleted.')  
      self.conn.commit()
    except Exception as e:
      print("Error in delete_all_tables: {e}")
    self.conn.close() 
  
  #This method create all tables and then insert the data in each table
  def create_table(self):
    schema.create_table()
    print("Table created successfully")
    sample.sample_data()
    print("Populated data successfully")

  #This method checks the pilot’s availability by retrieving data from the PilotAssignment and Pilot tables.
  def is_pilot_available(self, pilot_id):
    try:
        self.get_connection()
        self.cur.execute( """ SELECT *
                       FROM Pilot AS P
                       LEFT JOIN  PilotAssignment AS A 
                       ON P.pilot_id = A.pilot_id
                       WHERE A.flight_id IS NULL AND P.licence_expiry >= DATE('now', '+30 days') and P.pilot_id = ?;
                       """, (pilot_id,)
                       )
  
        row = self.cur.fetchone()
        return row is not None
    except Exception as e:
        print("Error in checking pilot availability  :", e)
        return False
    finally:
        self.conn.close()
  
  #This method checks flight availability by verifying whether a flight is scheduled and has not been assigned a pilot.
  def is_flight_available(self, flight_id):
    try:
        self.get_connection()
        self.cur.execute( """ SELECT * 
                         FROM Flight AS F
                         LEFT JOIN  PilotAssignment AS A 
                          ON   F.flight_id = A.flight_id
                        WHERE F.status_id = 1 AND A.assignment_id IS NULL AND F.flight_id = ?;
                       """, (flight_id,)
                       )
    
        row = self.cur.fetchone()
        return row is not None
    except Exception as e:
        print(" Error in checking flight availability",e)
        return False
    finally:
        self.conn.close()
  
  #This method assigns avaliable Pilot to a flight.
  def assign_avaliable_pilot(self):
    pilot_id = input("Enter pilot ID: ").strip()
    if not self.is_pilot_available(pilot_id):
        print('This pilot is not available for assignment.')
        return
    flight_id = str(input("Enter Flight ID (e.g.: 1): ")).strip()
    if not self.flight_exist(flight_id):
        print('This flight ID is not exist.')
        return
    if not self.is_flight_available(flight_id):
       print('This flight ID is not avaliable.')
       return
    try:
      self.get_connection()
      self.cur.execute( 
                        """  INSERT INTO PilotAssignment (pilot_id, flight_id)
                        VALUES (?, ?);
                        """, (pilot_id, flight_id,)
                       )
      self.conn.commit()
      print(f"Pilot ID:{pilot_id} assigned to Flight ID:{flight_id} the successfully.")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
 
 #This method checks the existence of a flight
  def flight_exist(self, flight_id):
    try:
      self.get_connection()
      self.cur.execute(
            """SELECT flight_id FROM Flight WHERE flight_id = ?""",
            (flight_id,)
        )
      row = self.cur.fetchone()
      if row is None:
          print(f"Flight ID:{flight_id} does not exist.")
          return False
      return True
    except Exception as e:
        print(f"Error in checking flight existence. {e}")
        return False

 #This method checks flight details by flight number
  def view_flight_no(self):
    try:
      self.get_connection()
      flight_no = str(input("Enter Flight Number (e.g.: FL003): ")).strip()
      if not re.match(r'^FL\d{3}$', flight_no):
        print("Invalid flight number . It should start 'FL' and followed by 3 numbers.")
        return
      self.cur.execute( 
                        """ SELECT F.flight_id ,F.flight_no, F.scheduled_departure,  R.origin_code, R.destination_code, S.status 
                       FROM Flight AS F 
                       JOIN Route R ON F.route_id = R.route_id 
                       JOIN FlightStatus AS S ON F.status_id = S.status_id
                       WHERE F.flight_no = ? """, (flight_no,) 
                       )
      row = self.cur.fetchall()
      if row is None:
        print("No flight found with the provided flight number.")
        return
      headers=["flight_id","flight_no", "scheduled_departure", "origin_code", "destination_code", "status_name"] 
      print(" ")
      print("-" * 50)
      print("Flight Information:")
      print(" ")
      print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
 
 #This method checks flight details by flight ID
  def view_flight_id(self):
    try:
      self.get_connection()
      flight_id = str(input("Enter Flight ID (e.g.: 1): ")).strip()
      if not self.flight_exist(flight_id):
        return
      print("1")
      self.cur.execute( 
                        """ SELECT F.flight_id ,F.flight_no, F.scheduled_departure,  R.origin_code, R.destination_code, S.status 
                       FROM Flight AS F 
                       JOIN Route R ON F.route_id = R.route_id 
                       JOIN FlightStatus AS S ON F.status_id = S.status_id
                       WHERE F.flight_id = ? """, (flight_id,) 
                       )
      row = self.cur.fetchall()
      if row is None:
        print("No flight found with the provided Flight ID.")
        return
      headers=["flight_id","flight_no", "scheduled_departure", "origin_code", "destination_code", "status_name"] 
      print(" ")
      print("-" * 50)
      print("Flight Information:")
      print(" ")
      print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

 #This method checks flight details by flight destination
  def view_flight_location(self):
    try:
      self.get_connection()
      origin = str(input("Enter origin of flight (e.g.: LHR): ")).strip().upper()
      
      if len(origin) !=3 or not origin.isalpha() :
        print("Invalid origin. Airport code should be 3 letters (e.g.: LHR).")
        return      
      destination = str(input("Enter destination of flight (e.g.: JFK): ")).strip().upper()
      
      if len(destination) !=3 or not destination.isalpha():
        print("Invalid destination. Airport code should be 3 letters (e.g.: LHR).")
        return  
      self.cur.execute( 
                        """ SELECT f.flight_no, f.scheduled_departure, r.origin_code,r.destination_code, s.status 
                       FROM Flight AS f 
                       JOIN Route r ON f.route_id = r.route_id 
                       JOIN FlightStatus s ON f.status_id = s.status_id
                       WHERE r.origin_code = ? AND r.destination_code = ? """, (origin,destination,) 
                       )
      row = self.cur.fetchone()
      if row is None:
        print("No flight found for the provided origin and destination.")
        return
      while row is not None:
        flight_no ,scheduled_departure, origin_code, destination_code,status_name = row   
        print(" ")
        print("-" * 50)
        print("Flight Information:")
        print(f"Flight Number: {flight_no}")
        print(f"Status: {status_name} ")
        print(f"Departs Origin: {origin_code} at {scheduled_departure}")
        print(f"Flight Destination: {destination_code}")
        row = self.cur.fetchone()
        print("-" * 50)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

#This method checks flight details by flight depature date
  def view_flight_date(self):
    try:
      self.get_connection()
      input_date = str(input("Enter depature date (e.g.: 2025-08-26): ")).strip()  
      self.cur.execute( 
                        """ SELECT f.flight_no, f.scheduled_departure,  r.origin_code,r.destination_code, s.status 
                       FROM Flight AS f 
                       JOIN Route r ON f.route_id = r.route_id 
                       JOIN FlightStatus s ON f.status_id = s.status_id
                       WHERE date(f.scheduled_departure) = ? """, (input_date,) 
                       )
      row = self.cur.fetchall()
      if row is None:
        print("No flight found for the provided date.")
        return
      headers =["flight_no", "scheduled_departure", "origin_code", "destination_code", "status" ] 
      print("-" * 50)
      print(f"Flights depart on {input_date}:")
      print(tabulate(row, headers, tablefmt="pretty")) 
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method adds a new flight record
  def new_flight(self):
    destination = input("Enter the destination airport code (e.g. BKK): ").strip().upper()
    route_id = self.retrive_route(destination)
    if not route_id:
        print(f"Currently ,we do not provide services to {destination}.")
        return
    scheduled_departure = input("Enter the scheduled departure time (YYYY-MM-DD HH:MM:SS): ")
    try:
        datetime.strptime(scheduled_departure, "%Y-%m-%d %H:%M:%S") 
    except ValueError:
        print("Invalid date and time format.Please enter time as YYYY-MM-DD HH:MM:SS")
        return
    try:
        self.get_connection()
        self.cur.execute(
            """INSERT INTO Flight ( route_id, scheduled_departure)
            VALUES (?, ?)""",
            ( route_id, scheduled_departure)
        )
        self.conn.commit()
        print(f"Flight information added successfully.")
    except Exception as e:
        print(f"Error adding flight: {e}")
    finally:
        self.conn.close()
  
  #This method checks flight details by flight status
  def view_flight_status(self):
    try:
      self.get_connection()
      status_list = ["Scheduled", "Delayed", "Boarding", "Boarding", "Departed", "Landed", "Arrived","Cancelled" ]
      print("Available flight statuses: ",status_list)
      input_status = str(input("Enter the status of flight (e.g.: Scheduled/Delayed): ")).strip().title()
      if  input_status not in status_list:
        print("Invalid status. Please enter a valid flight status.")
        return  
      self.cur.execute( 
                        """ SELECT f.flight_no, f.scheduled_departure, r.origin_code,r.destination_code, s.status 
                       FROM Flight AS f 
                       JOIN Route r ON f.route_id = r.route_id 
                       JOIN FlightStatus s ON f.status_id = s.status_id
                       WHERE s.status= ? """, (input_status,) 
                       )
      row = self.cur.fetchall()
      if row is None:
        print("No flight found with the provided status.")
        return
      print(" ")
      print("-" * 50)
      print(f"Flights that are {input_status}:")
      headers = ["flight_no", "scheduled_departure", "origin_code" , "destination_code", "status"]  
      print(tabulate(row, headers, tablefmt="pretty"))
       
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all flight details 
  def view_all_flight(self):
    try:
      self.get_connection()
      self.cur.execute( 
                        """ SELECT F.flight_id, F.flight_no, F.scheduled_departure,  R.origin_code, R.destination_code, S.status 
                       FROM Flight AS F 
                       JOIN Route AS R ON F.route_id = R.route_id 
                       JOIN FlightStatus AS S ON F.status_id = S.status_id;"""
                       )
      row = self.cur.fetchall()
      if row is None:
        print("No flight found .")
        return
      print(" ")
      print("-" * 50)
      print("Flight Information:")
      row_name =["flight_id", "flight_no", "scheduled_departure", "origin_code", "destination_code", "status"]
      print(tabulate(row, headers=row_name, tablefmt="pretty")) 
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all pilot details 
  def view_all_pilot(self):
    try:
      self.get_connection()
      
      self.cur.execute( """ SELECT count(*)
                       FROM  Pilot;"""
                      )
      total_pilot = self.cur.fetchone()[0]
      
      self.cur.execute( """ SELECT P.pilot_id, P.first_name, P.last_name, P.license_no, P.licence_expiry, R.rank_name
                       FROM  Pilot P
                       JOIN PilotRank R
                       ON P.rank_id = R.rank_id"""
                      )
      row = self.cur.fetchall()
      if row is None:
        print("No Pilot found .")
        return
      print("Pilot Information:")
      headers = ["Pilot ID", "First Name", "Last Name", "License No", "Licence Expiry", "Rank"]
      print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method adds all pilot details 
  def add_pilot(self):
    try:
      self.get_connection()
      input_first_name = str(input("Enter the first name of the pilot: ")).strip().title()
      input_last_name = str(input("Enter the last name of the pilot: ")).strip().title()
      input_license_no = str(input("Enter the license number of the pilot: ")).strip().upper()
      input_licence_expiry = str(input("Enter the licence expiry date of the pilot (YYYY-MM-DD): ")).strip()
      input_grade = str(input("Enter the grade of the pilot (e.g.: Captain/First Officer): ")).strip().title()
      if input_grade =='Captain':
        input_grade = 1
      elif input_grade == 'First Officer':
        input_grade = 2
      self.cur.execute( """ INSERT OR IGNORE INTO Pilot (first_name, last_name, license_no, licence_expiry, rank_id)
                            VALUES (?, ?, ?, ?, ?);""",
                        (input_first_name, input_last_name, input_license_no, input_licence_expiry, input_grade) )
      self.conn.commit()
      print("Pilot added successfully.")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all pilot details
  def view_all_route(self):
    try:
      self.get_connection()
      self.cur.execute( """ SELECT * FROM  Route""")
      row = self.cur.fetchall()
      if row is None:
        print("No Route table found .")
        return
      print("Route:")
      headers = ["route_id ", "origin_code ", "destination_code", "distance_miles", "duration_minutes "]
      print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all pilot assignment
  def view_all_assignment(self):
    try:
      self.get_connection()
      self.cur.execute( """ SELECT A.assignment_id,A.flight_id,A.pilot_id ,F.scheduled_departure 
                       FROM  PilotAssignment As A
                       JOIN Flight AS F ON A.flight_id = F.flight_id
                       """
                      )
      row = self.cur.fetchall()
      if row is None:
        print("No Pilot assignment found .")
        return
      print(" ")
      print("-" * 50)
      print("Pilot assignment schedule:")
      header = ["assignment_id", "flight_id", "pilot_id", "scheduled_departure"]
      print(tabulate(row, headers=header, tablefmt="pretty"))
      print(" ")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all pilot that have no assignment
  def view_no_assignment_pilot(self):
    try:
      self.get_connection()
    
      self.cur.execute( """ SELECT P.pilot_id ,P.rank_id 
                       FROM pilot P
                       LEFT JOIN  PilotAssignment A ON P.pilot_id = A.pilot_id
                       WHERE A.flight_id IS NULL AND P.licence_expiry >= DATE('now', '+30 days');
                       """)
    
      row = self.cur.fetchall()
      if row is None:
        print("No Pilot found .")
        return
      print(" ")
      print("-" * 50)
      print("Pilot with no assignment:")
      headers =["pilot_id", "pilot_rank" ]
      print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  #This method views all flight that have no pilot
  def view_flight_no_pilot(self):
    try:
      self.get_connection()
      self.cur.execute( 
                        """ SELECT F.flight_id
                       FROM Flight AS F 
                       LEFT JOIN PilotAssignment AS A 
                        ON  F.flight_id = A.flight_id
                       WHERE A.assignment_id  IS NULL 
                        AND F.status_id = 1 
                        """) 
      
      row = self.cur.fetchall()
      if row is None:   
        print("No Data found.All flights are assigned to pilots.")
        return
      print(" ")
      print("-" * 50)
      print("Flight pending to assign a pilot :")
      print("-" * 50)
      headers = ["flight_id"]
      print(tabulate(row, headers, tablefmt='pretty')) 
      
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method views all flight details dy destination
  def view_flight_by_destination(self):
    destination = str(input("Enter the flight destination airport code(e.g. BKK) to view Flight details: ").strip().upper())
    route_id = self.retrive_route(destination)
    print(route_id)
    try:
       self.cur.execute("""
                       SELECT F.flight_no, F.scheduled_departure, R.origin_code, R.destination_code, S.status 
                       FROM Flight AS F 
                       JOIN Route AS R ON F.route_id = R.route_id 
                       JOIN FlightStatus AS S ON F.status_id = S.status_id
                       WHERE F.route_id= ? """, (route_id,) 
                        )
       row = self.cur.fetchall()
       if row is None:
          print("There is no information was found regarding the provided destination.")
          return
       headers =["Flight_no", "scheduled_departure", "origin_code","destination_code", "status"]
       print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
        print(f"Error retrieving flight details for provided destination")
        return None
    finally:
        self.conn.close()

  #This method retrive flight's depature time by flight ID
  def retrive_depature_time(self, flight_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT scheduled_departure FROM Flight WHERE flight_id = ?""",
            (flight_id,)
        )
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            print(f"Flight number {flight_id} does not exist.")
            return None
    except Exception as e:
        print(f"Error retrieving departure for provided flight number")
        return None
    finally:
        self.conn.close()

  #This method verify flight's existence by flight ID
  def flight_exist(self, flight_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT flight_no FROM Flight WHERE flight_id = ?""",
            (flight_id,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"{flight_id} does not exist.")
            return False
        return True
    except Exception as e:
        print(f"Error in flight exist checking. Please try again. {e}")
        return False
  
  #This method update flight's status
  def update_flight_status(self):
    flight_id = input("Enter the flight ID(e.g. 1) to update status: ")
    if not self.flight_exist(flight_id):
        return 
    new_status = input("Enter the new status number (1.Scheduled, 2. Delayed, 3.Boarding , 4.Departed ,5.Landed,6.Arrived ,7.Cancelled ): ")
    if new_status not in ['1', '2', '3', '4', '5', '6', '7']:
        print("Invalid status number. Please enter a valid status number.")
        return
    try:
      self.get_connection()
      self.cur.execute( 
                        """ 
                        UPDATE Flight
                            SET status_id = ?
                            WHERE flight_id = ?
                            """,(new_status, flight_id)
                        ) 
      print(f"Flight {flight_id} status updated.")
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method update flight's depature time
  def update_departure_time(self):
    flight_id = input("Enter the flight id  (e.g. 1) to update departure time: ")
    if not self.flight_exist(flight_id):
        return
    new_depature = input("Enter the new departure time (e.g.HH:MM:SS) ): ").strip()
    try:
        datetime.strptime(new_depature,"%H:%M:%S")  
    except ValueError:
        print("Invalid time format.Please enter time as HH:MM:SS")
        return
    duration_minutes = self.retrive_flight_duration(self.retrive_flight_route(flight_id)) 
    try:
      self.get_connection()
      self.cur.execute( 
                        """ 
                        UPDATE Flight
                            SET scheduled_departure =  
                            DATE(scheduled_departure)|| ' ' || TIME(?)  
                            WHERE flight_id = ?
                            """,(new_depature ,flight_id)
                        ) 
      print( "Flight departure time updated successfully.")
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method retrives route id by destination_code
  def retrive_route(self, destination_code):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT route_id 
            FROM Route 
            WHERE destination_code = ?""" 
            ,(destination_code,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"Route to {destination_code} does not exist.")
            return False
        return row[0]
    except Exception as e:
        print(f"Error checking route existence: {e}")
        return False
 
 #This method update by destination 
  def update_destination (self):
    flight_id = input("Enter the flight ID(e.g. 1) to update status: ")
    if not self.flight_exist(flight_id):
        return
    new_destination = input("Enter the new destination airdport (e.g. BKK): ")
    route_id = self.retrive_route(new_destination)
    print(route_id)
    try:
      self.get_connection()
      self.cur.execute( 
                        """ 
                        UPDATE Flight
                            SET route_id = ?
                          WHERE flight_id = ?
                            """,
                            (route_id ,flight_id,)
                        ) 
      print( "Flight destination updated.")
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  #This method retrives destination_code by flight ID
  def retrive_destination(self, flight_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT destination_code FROM Route AS R
            JOIN Flight AS F ON R.route_id = F.route_id 
            WHERE F.flight_id = ?""",
            (flight_id,)
        )
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            print(f"Flight number does not exist.")
            return None
    except Exception as e:
        print(f"Error retrieving destination for provided flight number: {e}")
        return None
    finally:
        self.conn.close()
  
  #This method retrives duration id by route_id
  def retrive_flight_duration(self, route_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT duration_minutes 
            FROM Route 
            WHERE route_id = ?""",
            (route_id,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"Route ID does not exist.")
            return None
        return row[0]
    except Exception as e:
        print(f"Error retrieving flight duration: {e}")
        return None
    finally:
        self.conn.close()
  
  #This method retrives route_id id by flight_id
  def retrive_flight_route(self, flight_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT route_id FROM Flight WHERE flight_id = ?""",
            (flight_id,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"Flight ID does not exist.")
            return None
        return row[0]
    except Exception as e:
        print(f"Error retrieving flight route: {e}")
        return None
    finally:
        self.conn.close()

  #This method summarise the flight number of each destination
  def flight_destination_summary(self):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT R.destination_code ,COUNT(*) AS total_flight 
            FROM Flight AS F
            JOIN Route AS R ON F.route_id = R.route_id
            GROUP BY R.destination_code
            """
        )
        row = self.cur.fetchall()
        if row is None:
          print(f"No flights in each destination.")
          return 
        print("Flight Destination Summary:")
        headers = ["Destination Code", "Total Flights"]
        print(tabulate(row, headers, tablefmt="pretty"))
    except Exception as e:
        print(f"Error retrieving flight destination summary: {e}")
        return []
    finally:
        self.conn.close()
  
  #This method summarise the flight number of a Pilot
  def pilot_flight_summary(self):
    pilot_id = input("Enter the Pilot ID to calculate total flight been assigned: ")
    if not self.is_pilot_exists(pilot_id):
        return
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT COUNT(*)
            FROM PilotAssignment 
            WHERE pilot_id = ?""",
            (pilot_id,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"No flights found for this pilot.")
            return  
        print (f"There are {row[0]} flights assigned to this pilot")   
    except Exception as e:
        print(f"Error retrieving pilot's flight summary: {e}")
        return []
    finally:
        self.conn.close()
  
  #This method check the pilot assignment existence by flight id
  def assignment_exist(self,flight_id):
    try:
       self.get_connection()
       self.cur.execute(
          """SELECT * FROM PilotAssignment
            WHERE flight_id = ?""",
            (flight_id,)
           )
       row = self.cur.fetchone()
       if row is None:
          print(f"Flight ID:{flight_id} does not have any piolt assignment.")
          return False
    except Exception as e:
        print(f"Error. Please try again. {e}")
        return False
     
  #This method delete a pilot assignment by pilot id 
  def delete_pilot_assignment(self):
    pilot_id = input("Enter the pilot ID to remove assignment: ")
    if not self.is_pilot_exists(pilot_id):
        return
    flight_id = input("Enter the flight id (e.g.1) to remove pilot assignment: ")
    if not self.flight_exist(flight_id):
        return
    try:
        self.get_connection()
        self.cur.execute(
            """DELETE FROM PilotAssignment 
            WHERE flight_id = ? AND pilot_id = ?""",
            (flight_id,pilot_id)
        )
        self.conn.commit()
        print(f"Pilot ID : {pilot_id} has been removed from Flight ID: {flight_id}.")
    except Exception as e:
        print(f"Error removing pilot assignment: {e}")
    finally:
        self.conn.close()
  
  #This method verify pilot exisitneceby pilot id
  def is_pilot_exists(self, pilot_id):
    try:
        self.get_connection()
        self.cur.execute(
            """SELECT pilot_id 
            FROM Pilot 
            WHERE pilot_id = ?""",
            (pilot_id,)
        )
        row = self.cur.fetchone()
        if row is None:
            print(f"Pilot ID does not exist.")
            return False
        return True
    except Exception as e:
        print(f"Error in pilot existence: {e}")
        return False
    finally:
        self.conn.close()

  def assignment_exist(self,flight_id):
    try:
       self.get_connection()
       self.cur.execute(
          """SELECT * FROM PilotAssignment
            WHERE flight_id = ?""",
            (flight_id,)
           )
       row = self.cur.fetchone()
       if row is None:
          print(f"Flight ID:{flight_id} does not have any piolt assignment.")
          return False
    except Exception as e:
        print(f"Error. Please try again. {e}")
        return False

  def delete_flight_id(self):
    flight_id = input("Enter the flight id  (e.g. 1) to delete : ")
    if not self.flight_exist(flight_id):
        return
    try:
        if self.assignment_exist(flight_id):
                  self.cur.execute(
          """DELETE FROM PilotAssignment
            WHERE flight_id = ?""",
            (flight_id,)
           ) 
        print ("Flight and assignments deleted")   

        self.cur.execute(
          """DELETE FROM Flight
            WHERE flight_id = ?""",
            (flight_id,)
           )
        print ("Flight deleted")
        self.conn.commit()            
    except Exception as e:
            print(f"Error. Delete flight assignment.Please try again. {e}")
            return False


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.


while True:
  print("\n Menu:")
  print("**********")
  print(" 1.  Create tables and populate data")
  print(" 2.  Insert a new flight into Flight table")
  print(" 3.  Insert new pilot details")
  print(" 4.  View all flights and related info")
  print(" 5.  View all pilots and related info")
  print(" 6.  View all Pilot assignment schedules")
  print(" 7.  View all routes")
  print(" 8.  View pilots with no assignment")
  print(" 9.  View flights pending for pilots")  
  print(" 10. Assign an available pilot to flight") 
  print(" 11. View  flight details by Flight ID")   
  print(" 12. View  flight details by Flight Number") 
  print(" 13. View flights by destination")
  print(" 14. View flights by departure date") 
  print(" 15. View flights by status") 
  print(" 16. Update flights status")  
  print(" 17. Update a flight's departure time") 
  print(" 18. Update a flight's destination")
  print(" 19. Summarize total of flight of each destination") 
  print(" 20. Summarize total flight assignment of a pilot ") 
  print(" 21. Delete a pilot assignment")
  print(" 22. Delete a flight and its assignment by Flight ID")
  print(" 23. Drop all tables.")  
  print(" 24. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.new_flight()
  elif __choose_menu == 3:
    db_ops.add_pilot() 
  elif __choose_menu == 4:
    db_ops.view_all_flight()   
  elif __choose_menu == 5:
    db_ops.view_all_pilot()
  elif __choose_menu == 6:
    db_ops.view_all_assignment()
  elif __choose_menu == 7:
    db_ops.view_all_route()
  elif __choose_menu == 8:
    db_ops.view_no_assignment_pilot()
  elif __choose_menu == 9:
    db_ops.view_flight_no_pilot()     
  elif __choose_menu == 10:
    db_ops.assign_avaliable_pilot()
  elif __choose_menu == 11:
    db_ops.view_flight_id()    
  elif __choose_menu == 12:
    db_ops.view_flight_no()
  elif __choose_menu == 13:
    db_ops.view_flight_by_destination() 
  elif __choose_menu == 14:
    db_ops.view_flight_date()
  elif __choose_menu == 15:
    db_ops.view_flight_status()   
  elif __choose_menu == 16:
    db_ops.update_flight_status()
  elif __choose_menu == 17:
    db_ops.update_departure_time()
  elif __choose_menu == 18:
    db_ops.update_destination()
  elif __choose_menu == 19:
    db_ops.flight_destination_summary()
  elif __choose_menu == 20:
    db_ops.pilot_flight_summary()
  elif __choose_menu == 21:
    db_ops.delete_pilot_assignment()
  elif __choose_menu == 22:
    db_ops.delete_flight_id()
  elif __choose_menu == 23:
    db_ops.delete_all_tables()
  elif __choose_menu == 24:
    exit(0)
  else:
    print("Invalid Choice")
