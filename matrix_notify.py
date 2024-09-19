#!/usr/bin/env python3

import argparse
from enum import Enum
import json
import re
import requests # type: ignore
import subprocess
import sys
import uuid

DEFAULT_MATRIX_HOMESERVER_URL = "https://matrix-client.matrix.org"

class MatrixNotifier:
    """
    A class for sending messages to a Matrix room.

    Attributes:
        room_id (str): The ID of the Matrix room to send the message to.
        access_token (str): The access token used for authorization. (**Necessary if not using end-to-end encryption.**)
        homeserver_url (str): The URL of the Matrix homeserver. Defaults to `DEFAULT_MATRIX_HOMESERVER_URL`. (**Necessary if not using end-to-end encryption.**)

    ## Notes

    `room_id`: **You have to join** with this special account (hereinafter referred to as **bot account**) to **this room** before! (available in _room_ settings)

    ### Not using End-to-End Encryption (E2E)

    | Attribute        | example / additional information                                                                                                                                                                                                           |
    |------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `access_token`   | To get it in [Element](https://element.io/) for example, log in as the bot account, tap on the profile picture on the top left, and go to `All settings` → `Help & About`. There should be a dropdown menu on the bottom (`Access Token`)  |
    | `homeserver_url` | E.g. for a standard Matrix user `https://matrix-client.matrix.org` (available in _account_ settings)                                                                                                                                       |

    ### Using End-to-End Encryption (E2E)

    If you want to use E2E without carrying out the following steps, you will receive the following error messages:
    
    ```
    ERROR: matrix-commander: E153: Credentials file was not found. Provide credentials file or use --login to create a credentials file.
    INFO: matrix-commander: 1 error and 0 warnings occurred.
    ```

    #### [`matrix-commander`](https://github.com/8go/matrix-commander/tree/master) parameters

    | parameter      | description                         | example                            |
    |----------------|-------------------------------------|------------------------------------|
    | `device`       | name for the sending device         | `matrix-commander-notifier`        |
    | `user-login`   | your username                       | `@test:matrix.org`                 |
    | `password`     | login password for your bot account |                                    |
    | `homeserver`   | homeserver of your bot account      | `https://matrix-client.matrix.org` |
    | `room-default` | room id                             | `!xyz:matrix.org`                  |

    #### Setup

    A credentials file must be created for the `matrix-commander`. To do this, execute the following:

    ```
    matrix-commander --login PASSWORD --device 'REPLACE-ME' --user-login 'REPLACE-ME' --password 'REPLACE-ME' --homeserver 'REPLACE-ME' --room-default 'REPLACE-ME'
    ```

    **You have to replace all `REPLACE-ME` with your own credentials!**

    - To avoid mysterious errors, it is recommended to move the `credentials.json` file to the directory `$HOME/.config/matrix-commander/`.
    - Also create a storage directory: `$HOME/.local/share/matrix-commander/store/`

    (Reference: [matrix-commander](https://github.com/8go/matrix-commander/tree/master?tab=readme-ov-file#first-run-set-up-credentials-file-end-to-end-encryption))

    To verify a room session, once you have been invited and accepted into the room, you will need to go to the bot account in the room settings with the account you want to receive the encrypted messages with and verify the current session using emojis.

    In this case, it is better to start from a Matrix room of the account with which you want to receive the encrypted messages, for example.

    To verify a session immediately, send a message directly to a room:

    ```
    matrix-commander --room 'REPLACE-ME' -m 'First encrypted message :)'
    ```

    Therefore:

    ```
    matrix-commander --verify emoji
    ```

    **If you do not perform this step, the messages will be sent encrypted, but the session will not be verified and a warning will be displayed along with the message in messenger.**
    """
    
    def __init__(self, room_id: str, access_token: str = "", homeserver_url: str = DEFAULT_MATRIX_HOMESERVER_URL):
        self.room_id = room_id
        self.access_token = access_token
        self.homeserver_url = homeserver_url

    def send(self, message: str, use_e2e: bool = False) -> None:
        """
        Sends a message to the Matrix room.

        Args:
            message (str): The message to send to the Matrix room.
            use_e2e (bool): Whether to use end-to-end encryption. Defaults to `False`.
        """

        error_message_part_for_empty_or_whitespace = "Cannot be empty or just whitespace:"

        def _is_empty_or_whitespace(var) -> bool:
            return not bool(var.strip())

        if _is_empty_or_whitespace(message):
            print(f"{error_message_part_for_empty_or_whitespace} Message")
            sys.exit(1)

        def _is_valid_room_id() -> bool:
            # Regex: Room ID must start with '!', contain at least one ':'
            pattern = r'^![^:]+:[^:]+$'
            return re.match(pattern, self.room_id) is not None

        if not _is_valid_room_id():
            print(f"Invalid room ID: {self.room_id}. It must start with '!' and contain a ':'.")
            sys.exit(1)

        def _send_without_e2e(message_html, room_id, homeserver_url, access_token):
            if _is_empty_or_whitespace(homeserver_url):
                raise Exception(f"{error_message_part_for_empty_or_whitespace} Homeserver url")

            if _is_empty_or_whitespace(access_token):
                raise Exception(f"{error_message_part_for_empty_or_whitespace} Access token")

            def _strip_html_tags_and_non_ascii_characters(html_message: str) -> str:
                plain_text = re.sub(r'<.*?>', '', html_message)
                plain_text = re.sub(r'[^\x00-\x7F]+', '', plain_text)
                return plain_text

            message_data = {
                "msgtype": "m.text",
                "body": _strip_html_tags_and_non_ascii_characters(message_html),
                "format": "org.matrix.custom.html",
                "formatted_body": message_html,
            }
            message_data_json = json.dumps(message_data).encode("utf-8")
            authorization_headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json", "Content-Length": str(len(message_data_json))}
            request = requests.put(url=f"{homeserver_url}/_matrix/client/r0/rooms/{room_id}/send/m.room.message/{str(uuid.uuid4())}", data=message_data_json, headers=authorization_headers)

            if request.status_code != 200:
                raise Exception(f"Status code: {request.status_code}.\nResponse: {request.text}")

        def _send_with_e2e(message_html, room_id):
            command = [
                "matrix-commander",
                "-m", message_html,
                "--room", room_id,
                "--html",
            ]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                raise Exception(f"{e}")

        try:
            if not use_e2e:
                _send_without_e2e(message, self.room_id, self.homeserver_url, self.access_token)
            else:
                _send_with_e2e(message, self.room_id)
            print(f"Message '{message}' sent successfully to room '{self.room_id}' ({'with' if use_e2e else 'without'} E2E).")
        except Exception as e:
            print(f"An error occurred while sending the message '{message}' to room '{self.room_id}' ({'with' if use_e2e else 'without'} E2E):\n{e}")
            sys.exit(1)

class Helper:
    '''
    A helper class for various tasks.
    '''
    class HTML:
        '''
        A helper class for HTML-related tasks. This makes it easier to format messages for Matrix.
        '''
        class Tag(Enum):
            '''
            Enum for HTML tags.

            Attributes:
                H1 (str):
                    `h1` (HTML: `<h1>...</h1>`).
                H2 (str):
                    `h2` (HTML: `<h2>...</h2>`).
                H3 (str):
                    `h3` (HTML: `<h3>...</h3>`).
                H4 (str):
                    `h4` (HTML: `<h4>...</h4>`).
                PARAGRAPH (str):
                    `p` (HTML: `<p>...</p>`).
                CODE (str):
                    `code` (HTML: `<pre><code>...</code></pre>`).
                BOLD (str):
                    `strong` (HTML: `<strong>...</strong>`).
                ITALIC (str):
                    `em` (HTML: `<em>...</em>`).

            ## Notes

            - `format`: Formats the content with the corresponding tag.
            - `replace_new_lines`: Replaces new lines with `<br>`.
            - `replace_spaces`: Replaces spaces with `&nbsp;`.
            - `replace_spaces_and_new_lines`: Replaces spaces and new lines with `<br>` and `&nbsp;` respectively.
            '''
            H1 = "h1"
            H2 = "h2"
            H3 = "h3"
            H4 = "h4"
            PARAGRAPH = "p"
            CODE = "code"
            BOLD = "strong"
            ITALIC = "em"

            def format(self, content: str) -> str:
                '''
                Formats the content with the corresponding tag.

                Args:
                    content (str): The content to format.

                Returns:
                    str: The formatted content.
                
                Example:
                    >>> Helper.HTML.Tag.H1.format("Hello, world!")
                    <h1>Hello, world!</h1>
                '''
                try:
                    if self == Helper.HTML.Tag.H1:
                        return f"<h1>{content}</h1>"
                    elif self == Helper.HTML.Tag.H2:
                        return f"<h2>{content}</h2>"
                    elif self == Helper.HTML.Tag.H3:
                        return f"<h3>{content}</h3>"
                    elif self == Helper.HTML.Tag.H4:
                        return f"<h4>{content}</h4>"
                    elif self == Helper.HTML.Tag.PARAGRAPH:
                        return f"<p>{content}</p>"
                    elif self == Helper.HTML.Tag.CODE:
                        return f"<pre><code>{content}</code></pre>"
                    elif self == Helper.HTML.Tag.BOLD:
                        return f"<strong>{content}</strong>"
                    elif self == Helper.HTML.Tag.ITALIC:
                        return f"<em>{content}</em>"
                    else:
                        raise ValueError(f"Unsupported tag '{self}'")
                except ValueError as ve:
                    print(f"'ValueError' in 'format': {ve}")
                    return content
                except Exception as e:
                    print(f"An unexpected error occurred in 'format': {e}")
                    return content

        @staticmethod
        def replace_new_lines(content: str) -> str:
            '''
            Replaces new lines with `<br>`.

            Args:
                content (str): The content to replace new lines in.
            
            Returns:
                str: The content with new lines replaced with `<br>`.
            '''
            return content.replace("\n", "<br>")

        @staticmethod
        def replace_spaces(content: str) -> str:
            '''
            Replaces spaces with `&nbsp;`.

            Args:
                content (str): The content to replace spaces in.

            Returns:
                str: The content with spaces replaced with `&nbsp;`.
            '''
            return content.replace(" ", '&nbsp;')

        @staticmethod
        def replace_spaces_and_new_lines(content: str) -> str:
            '''
            Replaces spaces and new lines with `<br>` and `&nbsp;` respectively.

            Args:
                content (str): The content to replace spaces and new lines in.

            Returns:
                str: The content with spaces replaced with `&nbsp;` and new lines replaced with `<br>`.
            '''
            return Helper.HTML.replace_new_lines(Helper.HTML.replace_spaces(content))

def _process_arguments() -> argparse.Namespace:
    note_for_e2e = "Not necessary if '--use-e2e' is unused or set to 'False'."

    parser = argparse.ArgumentParser(description="Send a message to a Matrix room, optionally with end-to-end encryption. For more information, especially on the use of end-to-end encryption, see: https://github.com/fuchs-fabian/matrix-notify-py")

    parser.add_argument('--use-e2e', type=str, default="False", help="Use end-to-end encryption for sending messages. (case-insensitive, Default: 'False')")
    parser.add_argument('--message', type=str, required=True, help="The message to send to the Matrix room.")
    parser.add_argument('--room-id', type=str, required=True, help="Matrix room ID. (Something like '!xyz:matrix.org')")
    parser.add_argument('--homeserver-url', type=str, default=DEFAULT_MATRIX_HOMESERVER_URL, help=f"{note_for_e2e} Matrix homeserver URL. (Default: '{DEFAULT_MATRIX_HOMESERVER_URL}')")
    parser.add_argument('--access-token', type=str, help=f"{note_for_e2e} Matrix access token.")

    args=parser.parse_args()

    use_e2e = args.use_e2e.strip().lower() == 'true'

    if not use_e2e:
        if not args.access_token:
            print("Access token is required for sending messages without E2E.")
            sys.exit(1)
        if not args.homeserver_url:
            print("Homeserver URL is required for sending messages without E2E.")
            sys.exit(1)

    args.use_e2e = use_e2e
    return args

def _process_arguments_and_send_message():
    args = _process_arguments()

    notifier = MatrixNotifier(
        room_id=args.room_id,
        access_token=args.access_token,
        homeserver_url=args.homeserver_url,
    )

    notifier.send(args.message, args.use_e2e)

if __name__ == "__main__":
    _process_arguments_and_send_message()