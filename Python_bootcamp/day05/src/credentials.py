from html import escape
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

species = {
    "Cyberman": "John Lumic",
    "Dalek": "Davros",
    "Judoon": "Shadow Proclamation Convention 15 Enforcer",
    "Human": "Leonardo da Vinci",
    "Ood": "Klineman Halpen",
    "Silence": "Tasha Lem",
    "Slitheen": "Coca-Cola salesman",
    "Sontaran": "General Staal",
    "Time Lord": "Rassilon",
    "Weeping Angel": "The Division Representative",
    "Zygon": "Broton"
}

def application (environ, start_response):
    response_headers = [('Content-Type', 'application/json')]
    
    parsed_string = parse_qs(environ["QUERY_STRING"])
    credentials = parsed_string.get("species", [''])[0]
    credentials = escape(credentials)
    
    if credentials in species:
        default_status = "202 "
        response_body = {"credentials": species[credentials]}
    else:
        default_status = "404 "
        response_body = {"credentials": "Unknown"}
    
    start_response(default_status, response_headers)
    return [json.dumps(response_body).encode("utf-8")]

httpd = make_server('localhost', 8888, application)
httpd.serve_forever()    