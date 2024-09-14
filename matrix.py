#!/usr/bin/env python3

import json
import uuid
import requests
import subprocess

USE_E2E = True

MATRIX_HOMESERVER_URL = "https://matrix-client.matrix.org"
MATRIX_ACCESS_TOKEN = ""
MATRIX_ROOM_ID = ""

def create_messages():
    message = (
        f"Hello World!"
    )

    message_html = (
        f"<b>Hello World!</b>"
    )
    return message, message_html

def send_with_e2e(message_html, room_id):
    command = [
        "matrix-commander",
        "-m", message_html,
        "--room", room_id,
        "--html",
    ]

    try:
        subprocess.run(command, check=True)
        print("Message sent successfully (with E2E).")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message (with E2E). Error: {e}")

def send_without_e2e(message, message_html, homeserver_url, access_token, room_id):
    message_data = {
        "msgtype": "m.text",
        "body": message,
        "format": "org.matrix.custom.html",
        "formatted_body": message_html,
    }
    message_data_json = json.dumps(message_data).encode("utf-8")
    authorization_headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json", "Content-Length": str(len(message_data_json))}

    request = requests.put(url=f"{homeserver_url}/_matrix/client/r0/rooms/{room_id}/send/m.room.message/{str(uuid.uuid4())}", data=message_data_json, headers=authorization_headers)

    if request.status_code == 200:
        print("Message sent successfully (without E2E).")
    else:
        print(f"Failed to send message (without E2E). Status code: {request.status_code}")

try:
    message, message_html = create_messages()
    if USE_E2E:
        send_with_e2e(message_html, MATRIX_ROOM_ID)
    else:
        send_without_e2e(message, message_html, MATRIX_HOMESERVER_URL, MATRIX_ACCESS_TOKEN, MATRIX_ROOM_ID)
except Exception as e:
    print(f"An error occurred: {e}")