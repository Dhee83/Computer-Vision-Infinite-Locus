import cv2
import base64
import websocket
import json

endpoint_url = "ws://localhost:8000/ws/data/"

def send_frame(frame):
    ws = init_ws()

    payload = {
        'data': frame
    }

    ws.send(json.dumps(payload))


def on_message(ws, message):
    print(f"Received message: {message}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws):
    print("Connection closed")



def init_ws():

    ws = websocket.WebSocket()


    ws.on_message = on_message
    ws.on_error = on_error
    ws.on_close = on_close


    ws.connect(endpoint_url)
    return ws




