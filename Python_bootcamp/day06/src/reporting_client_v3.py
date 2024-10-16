from __future__ import print_function
import logging
from sqlalchemy.orm import Session

# Necessary modules:
import sys
import grpc
import models
import report_pb2
import arguments
import sqlalchemy
import report_pb2_grpc

logging.basicConfig(level=logging.DEBUG)

class_list = ["Corvette", "Frigate", "Cruiser", "Destroyer", "Carrier", "Dreadnought"]

def bytes_to_alignment(alignment: int):
    if alignment == 0:
        return "Ally"
    elif alignment == 1:
        return "Enemy"

def checker(spaceship):
    if ((spaceship.type == "Corvette") and (80 <= spaceship.length <= 250) and (4 <= spaceship.crew_size <= 10) and
            spaceship.armed):
        return True
    elif ((spaceship.type == "Frigate") and (300 <= spaceship.length <= 600) and (10 <= spaceship.crew_size <= 15) and
        spaceship.armed and (spaceship.alignment == "Ally")):
        return True
    elif ((spaceship.type == "Cruiser") and (500 <= spaceship.length <= 1000) and (15 <= spaceship.crew_size <= 30) and
        spaceship.armed):
        return True
    elif ((spaceship.type == "Destroyer") and (800 <= spaceship.length <= 2000) and (50 <= spaceship.crew_size <= 80)
        and spaceship.armed and (spaceship.alignment == "Ally")):
        return True
    elif ((spaceship.type == "Carrier") and (1000 <= spaceship.length <= 4000) and (120 <= spaceship.crew_size <= 250)
        and (not spaceship.armed)):
        return True
    elif ((spaceship.type == "Dreadnought") and (5000 <= spaceship.length <= 20000)
        and (300 <= spaceship.crew_size <= 500) and spaceship.armed):
        return True
    else:
        return False

def add_traitor(engine, first_name, last_name, rank):
    with Session(engine) as session:
        new_traitor = models.Traitor(
            first_name=first_name,
            last_name=last_name,
            rank=rank
        )

        session.add(new_traitor)
        session.commit()
        session.close()

def is_exist_traitor(engine, first_name, last_name, rank):
    session = Session(engine)

    for traitor in session.query(models.Traitor):
        if (traitor.first_name == first_name) and (traitor.last_name == last_name) and (traitor.rank == rank):
            session.close()
            return True

    session.close()

    return False

def find_traitors(engine):
    session = Session(engine)

    for officer in session.query(models.Officer):
        for second_officer in session.query(models.Officer):
            if ((officer.last_name == second_officer.last_name) and
                    (officer.first_name == second_officer.first_name) and (officer.rank == second_officer.rank) and
                    (officer.status != second_officer.status) and not
                    is_exist_traitor(engine, second_officer.first_name, second_officer.last_name,
                                     second_officer.rank)):
                add_traitor(engine, officer.first_name, officer.last_name, officer.rank)

                print("{ first_name: " + officer.first_name +
                ", last_name: " + officer.last_name +
                ", rank: " + officer.rank +
                " }"
                )
                session.close()

def create_connection(USER_NAME: str, USER_PASSWORD: str, DATABASE_NAME: str):
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://" + USER_NAME + ":" + USER_PASSWORD + "@localhost/" +
                                      DATABASE_NAME)
    engine.connect()

    return engine

def create_tables(engine):
    models.Base.metadata.create_all(engine)


def delete_tables(engine):
    models.Base.metadata.drop_all(engine)

def find_officers(engine, spaceship_index):
    session = Session(engine)
    answer = '['

    for officer in session.query(models.Officer):
        if officer.spaceship_id == spaceship_index:
            answer = answer + '{ first_name: ' + str(officer.first_name) + ', '
            answer = answer + 'last_name: ' + str(officer.last_name) + ', '
            answer = answer + 'rank: ' + str(officer.rank) + ' }, '

    session.close()

    if answer == "{":
        return ""
    else:
        return answer[:-2] + ']'

def add_spaceship(engine, spaceship):
    with Session(engine) as session:
        session.add(spaceship)
        session.commit()
        session.close()

        
def add_officer(engine, officer, spaceship_id, status):
    with Session(engine) as session:
        existing_officer = session.query(models.Officer).filter(
            models.Officer.spaceship_id == spaceship_id,
            models.Officer.first_name == officer.first_name,
            models.Officer.last_name == officer.last_name,
            models.Officer.rank == officer.rank
        ).first()
        
        if existing_officer:
            # Обновляем существующую запись
            existing_officer.spaceship_id = spaceship_id
            existing_officer.status = status
        else:
            # Создаем новую запись
            new_officer = models.Officer(
                first_name=officer.first_name,
                last_name=officer.last_name,
                rank=officer.rank,
                spaceship_id=spaceship_id,
                status=status
            )
            session.add(new_officer)
        
        session.commit()
        
def find_last_status(engine):
    status = []
    session = Session(engine)

    for spaceship in session.query(models.Spaceship):
        status.append(spaceship.alignment)

    session.close()

    if len(status) > 0:
        return status[-1]

    return "Ally"

def find_last_index(engine):
    index = []
    session = Session(engine)

    for spaceship in session.query(models.Spaceship):
        index.append(spaceship.id)

    session.close()

    if len(index) > 0:
        return index[-1]

    return -1

def print_traitors(engine):
    session = Session(engine)
    print("\nList of traitors: \n")
    for traitor in session.query(models.Traitor):
        print("{ first_name: " + traitor.first_name +
              ", last_name: " + traitor.last_name +
              ", rank: " + traitor.rank +
              " }"
              )

    session.close()
    
def print_spaceships(engine):
    session = Session(engine)

    for spaceship in session.query(models.Spaceship):
        if checker(spaceship):
            print("{ alignment: " + spaceship.alignment +
                  ", name: " + spaceship.name +
                  ", class: " + spaceship.type +
                  ", length: " + str(spaceship.length) +
                  ", crew_size: " + str(spaceship.crew_size) +
                  ", armed: " + spaceship.armed +
                  ", officers: " + find_officers(engine, spaceship.id) +
                  " }"
                  )

    session.close()

def run():
    if (len(sys.argv) == 2) and (sys.argv[-1] == "list_traitors"):  # list traitors case
        engine = create_connection(arguments.USER_NAME, arguments.USER_PASSWORD, arguments.DATABASE_NAME)
        create_tables(engine)
        print_traitors(engine)
        
    # elif sys.argv[1] == "scan":  # scan case
    #     args = args = sys.argv[2:]
    #     try:
    #         coordinates = []
    #         for arg in args:                
    #             # Replace non-standard minus signs with standard minus sign
    #             arg = str(arg.replace('\u2009', ' ').replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-'))
                
    #             # Replace comma with dot if comma is used
    #             arg = arg.replace(',', '.')
                
    #             # Convert to float
    #             try:
    #                 coords = [float(x) for x in arg.split()]
    #                 coordinates.extend(coords)
    #             except ValueError as ve:
    #                 print(f"Error converting '{arg}' to float: {ve}")
    #                 raise
            
    #         print(f"All coordinates: {coordinates}")
            
    #         if (len(coordinates) == 2) or (len(coordinates) == 6):
    #             engine = create_connection(arguments.USER_NAME, arguments.USER_PASSWORD, arguments.DATABASE_NAME)

    #             create_tables(engine)
    #             find_traitors(engine)
                           
    #         else:
    #             print(f"ERROR! INCORRECT COUNT OF ARGUMENTS. Expected 2 or 6.")
    #             return
            
    #     except ValueError:
    #         print("ERROR! INCORRECT TYPES OF ARGUMENTS.")
    
    else:
        if sys.argv[1] == "scan":
            args = sys.argv[2:]
        else:
            args = sys.argv[1:]
        
        try:
            coordinates = []
            for arg in args:                
                # Replace non-standard minus signs with standard minus sign
                arg = str(arg.replace('\u2009', ' ').replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-'))
                
                # Replace comma with dot if comma is used
                arg = arg.replace(',', '.')
                
                # Convert to float
                try:
                    coords = [float(x) for x in arg.split()]
                    coordinates.extend(coords)
                except ValueError as ve:
                    print(f"Error converting '{arg}' to float: {ve}")
                    raise
            
            print(f"All coordinates: {coordinates}")
                     
            if len(coordinates) == 2:
                lat, lon = coordinates
                
            elif len(coordinates) == 6:
                lat, _, _, lon, _, _ = coordinates
            
            else:
                print(f"ERROR! INCORRECT COUNT OF ARGUMENTS. Expected 2 or 6.")
                return
            
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                try:
                    engine = create_connection(arguments.USER_NAME, arguments.USER_PASSWORD,
                                                arguments.DATABASE_NAME)
                    # delete_tables(engine)  # If you want to clear database
                    create_tables(engine)
                except Exception as e:
                    logging.error(f"Failed to connect to database: {e}")
                    exit()
                                
                try:
                    channel = grpc.insecure_channel("localhost:55555")
                    stub = report_pb2_grpc.ReportingServiceStub(channel)
                    for ship in stub.GetShips(report_pb2.Coordinate(values=coordinates)):
                                        
                        spaceship = models.Spaceship(
                            alignment=bytes_to_alignment(ship.alignment),
                            name=ship.name,
                            type=class_list[ship.type],
                            length=float(ship.length),
                            crew_size=ship.size,
                            armed=ship.armed,
                        )

                        if checker(spaceship):
                            add_spaceship(engine, spaceship)

                            for officer in ship.officers:
                                index = find_last_index(engine)
                                status = find_last_status(engine)
                                add_officer(engine, officer, index, status)

                    print_spaceships(engine)
                    if sys.argv[1] == "scan":
                        print("\nFound traitors: ")
                        find_traitors(engine)
                    channel.close()

                
                except grpc.RpcError as rpc_err:
                    logging.error(f"gRPC RPC Error: {rpc_err}")
                except Exception as e:
                    logging.exception(f"An error occurred: {e}")
                
            else:
                print("ERROR! INCORRECT COORDINATES.")
                
        except Exception as e:
                logging.exception(f"An error occurred: {e}")
                print("ERROR! INCORRECT TYPE OF ARGUMENTS!")


if __name__ == "__main__":
    run()
    