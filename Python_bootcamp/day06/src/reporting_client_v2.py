import json
import sys
import grpc
import report_pb2
import report_pb2_grpc
from typing import List
from pydantic import BaseModel


alignment_list = ["Ally", "Enemy"]
class_list = ["Corvette", "Frigate", "Cruiser", "Destroyer", "Carrier", "Dreadnought"]


def bytes_to_alignment(alignment):
    return alignment_list[alignment]


def bytes_to_class(class_):
    return class_list[class_]

class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str


class Spaceship(BaseModel):
    alignment: str
    name: str
    type: str
    length: float
    crew_size: int
    armed: bool

    officers: List[Officer]

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

def run():
    args = sys.argv[1:]
   
    with grpc.insecure_channel("localhost:55555") as channel:
        stub = report_pb2_grpc.ReportingServiceStub(channel)

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
                for ship in stub.GetShips(report_pb2.Coordinate(values=coordinates)):
                    officers = []
                    for i in ship.officers:
                        officers.append(Officer(first_name=i.first_name, last_name=i.last_name, rank=i.rank))
  
                    spaceship = Spaceship(
                        alignment=bytes_to_alignment(ship.alignment),
                        name=ship.name,
                        type=bytes_to_class(ship.type),
                        length=round(ship.length, 1),
                        crew_size=ship.size,
                        armed=ship.armed,
                        officers=officers
                    )
                                           
                    if checker(spaceship):
                        ship_dict = spaceship.model_dump()
            
                        # Форматируем JSON с отступами и переносами строк
                        formatted_json = json.dumps(ship_dict, indent=2, sort_keys=True)
            
                        # Выводим форматированный JSON
                        print(formatted_json)
                        print("\n")
            else:
                print("ERROR! INCORRECT COORDINATES.")

        except ValueError as ve:
            print(f"VALUE ERROR: {ve}")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")
            
if __name__ == "__main__":
    run()