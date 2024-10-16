# Necessary modules:
from concurrent import futures

import grpc
import random
import report_pb2
import report_pb2_grpc

# Ship data:
ship_list = ["Normandy", "Executor", "Rocket", "Starship", "Probe", "Juno", "Hubble", "Viking", "Spirit", "Unknown"]

# Officer data:
name_list = ["Alan", "Abbe", "Abbot", "Abel", "Aberdeen", "Abner"]
surname_list = ["Shepard", "Bothell", "Carroll", "Farrell", "James", "Keat"]
rank_list = ["Marshal", "Captain", "Major", "General", "Colonel"]


class ReportingServiceServicer(report_pb2_grpc.ReportingServiceServicer):
    def GetShips(self, request, context):
        # Check coordinate data:
        if len(request.values) in [2, 6]:
            for _ in range(random.randint(0, 100)):
                ship = report_pb2.Spaceship()  # Create new ship

                # Fill ship data:
                ship.alignment = random.randint(0, 1)

                # Check case with "Unknown" case:
                if ship.alignment == 1:
                    ship.name = random.choice(ship_list)
                else:
                    ship.name = random.choice(ship_list[:-1])

                ship.type = random.randint(0, 5)
                ship.length = random.randint(0, 20000) + round(random.random(), 1)
                ship.size = random.randint(1, 650)
                ship.armed = bool(random.randint(0, 1))

                # Fill officers:
                for __ in range(random.randint(0, 10)):
                    officer = ship.officers.add()

                    officer.first_name = random.choice(name_list)
                    officer.last_name = random.choice(surname_list)
                    officer.rank = random.choice(rank_list)

                yield ship


def serve():  # Function for working the server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    report_pb2_grpc.add_ReportingServiceServicer_to_server(ReportingServiceServicer(), server)
    server.add_insecure_port("[::]:55555")
    server.start()
    server.wait_for_termination()


# Test case:
if __name__ == "__main__":
    serve()