from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import json
from execute import execute_request

HOST = "0.0.0.0" # Listen from all addresses
PORT = 8000

app = FastAPI()

decoder = json.JSONDecoder()

@app.post("/server")
async def server(request: Request):
    raw_body = await request.body()
    text_data = raw_body.decode("utf-8")
    query_type, payload = parse_request(text_data)

    #print("Received:",payload)

    response = {"response":execute_request(query_type, payload)}
 
    #print(response)

    return response

def parse_request(text_data):
    # query=wasd&payload=CMON DO SOMETHING
    query_type = text_data.split('=')[1].split('&')[0]
    # DEBUG
    #print(get_payload(text_data, len(query_type)))
    payload = get_payload(text_data, len(query_type)) #decoder.decode(text_data.split('=')[2])
    return (query_type, payload)

def get_payload(text_data, query_type_len):
    payload = decoder.decode(text_data[6+query_type_len+9:])
    return payload

def make_response(response_txt):
    return {"response":response_txt}

def startup_message():
    # Source - https://stackoverflow.com/a/166589
    # Posted by UnkwnTech, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-10-23, License - CC BY-SA 3.0
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("\n###")
    url = "http://{}/server".format(s.getsockname()[0])
    print("Server URL is '{}'".format(url))
    print("###")
    print()
    s.close()

if __name__ == "__main__":
    startup_message()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
