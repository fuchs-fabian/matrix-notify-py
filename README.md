# `matrix-notify-py`: Simple Python script for sending HTML messages to a Matrix room, optionally with E2E

<p align="center">
  <a href="./LICENSE">
    <img alt="GPL-3.0 License" src="https://img.shields.io/badge/GitHub-GPL--3.0-informational">
  </a>
</p>

<div align="center">
  <table>
    <tr>
      <td>
        <a href="https://github.com/fuchs-fabian/matrix-notify-py">
          <img src="https://github-readme-stats.vercel.app/api/pin/?username=fuchs-fabian&repo=matrix-notify-py&theme=holi&hide_border=true&border_radius=10" alt="Repository matrix-notify-py"/>
        </a>
      </td>
    </tr>
  </table>
</div>

## Description

Simple Python script for sending HTML messages to a [Matrix](https://matrix.org/) room, optionally with E2E.

By importing this package, you can focus solely on the logic without worrying how to handle the notifier logic.

## Getting Started

> It is possible that `pip` is not yet installed. If this is not the case, you will be prompted to install it. Confirm the installation.

### Installation with `pip` (GitHub)

```bash
pip install git+https://github.com/fuchs-fabian/matrix-notify-py.git
```

### Installation with `pip` (Local)

Download the repository and navigate to the directory containing the [`setup.py`](setup.py) file.

```bash
pip install .
```

### Check Installation

```bash
pip list
```

```bash
pip show matrix-notify
```

### Usage

#### Python

```python
#!/usr/bin/env python3

import matrix_notify as mn

def main():
    notifier = mn.MatrixNotifier(
        room_id="!your_room_id:your_homeserver",
        #access_token="your_access_token",                  # Neccessary if using not E2E
        #homeserver_url=mn.DEFAULT_MATRIX_HOMESERVER_URL,   # Neccessary if using not E2E
    )

    # Your logic here
    # ...
    # e.g.
    message = mn.Helper.HTML.Tags.H1.format("Hello World")
    message = mn.Helper.HTML.replace_spaces(message)

    notifier.send(message, True)

if __name__ == "__main__":
    main()
```

#### Command Line

```plain
usage: matrix-notify [-h] [--use-e2e USE_E2E] --message MESSAGE --room-id ROOM_ID [--homeserver-url HOMESERVER_URL]
                     [--access-token ACCESS_TOKEN]

Send a message to a Matrix room, optionally with end-to-end encryption. For more information, especially on the use of end-to-end
encryption, see: https://github.com/fuchs-fabian/matrix-notify-py

options:
  -h, --help            show this help message and exit
  --use-e2e USE_E2E     Use end-to-end encryption for sending messages. (case-insensitive, Default: 'False')
  --message MESSAGE     The message to send to the Matrix room.
  --room-id ROOM_ID     Matrix room ID. (Something like '!xyz:matrix.org')
  --homeserver-url HOMESERVER_URL
                        Not necessary if '--use-e2e' is unused or set to 'False'. Matrix homeserver URL. (Default:
                        'https://matrix-client.matrix.org')
  --access-token ACCESS_TOKEN
                        Not necessary if '--use-e2e' is unused or set to 'False'. Matrix access token.
```

### Notes

`room_id`: **You have to join** with this special account (hereinafter referred to as **bot account**) to **this room** before! (available in _room_ settings)

#### Not using End-to-End Encryption (E2E)

| Attribute        | example / additional information                                                                                                                                                                                                           |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `access_token`   | To get it in [Element](https://element.io/) for example, log in as the bot account, tap on the profile picture on the top left, and go to `All settings` → `Help & About`. There should be a dropdown menu on the bottom (`Access Token`)  |
| `homeserver_url` | E.g. for a standard Matrix user `https://matrix-client.matrix.org` (available in _account_ settings)                                                                                                                                       |

#### Using End-to-End Encryption (E2E)

If you want to use E2E without carrying out the following steps, you will receive the following error messages:

```plain
ERROR: matrix-commander: E153: Credentials file was not found. Provide credentials file or use --login to create a credentials file.
INFO: matrix-commander: 1 error and 0 warnings occurred.
```

##### [`matrix-commander`](https://github.com/8go/matrix-commander/tree/master) parameters

| parameter      | description                         | example                            |
|----------------|-------------------------------------|------------------------------------|
| `device`       | name for the sending device         | `matrix-commander-notifier`        |
| `user-login`   | your username                       | `@test:matrix.org`                 |
| `password`     | login password for your bot account |                                    |
| `homeserver`   | homeserver of your bot account      | `https://matrix-client.matrix.org` |
| `room-default` | room id                             | `!xyz:matrix.org`                  |

##### Setup

A credentials file must be created for the `matrix-commander`. To do this, execute the following:

```plain
matrix-commander --login PASSWORD --device 'REPLACE-ME' --user-login 'REPLACE-ME' --password 'REPLACE-ME' --homeserver 'REPLACE-ME' --room-default 'REPLACE-ME'
```

**You have to replace all `REPLACE-ME` with your own credentials!**

- To avoid mysterious errors, it is recommended to move the `credentials.json` file to the directory `$HOME/.config/matrix-commander/`.
- Also create a storage directory: `$HOME/.local/share/matrix-commander/store/`

(Reference: [matrix-commander](https://github.com/8go/matrix-commander/tree/master?tab=readme-ov-file#first-run-set-up-credentials-file-end-to-end-encryption))

To verify a room session, once you have been invited and accepted into the room, you will need to go to the bot account in the room settings with the account you want to receive the encrypted messages with and verify the current session using emojis.

In this case, it is better to start from a Matrix room of the account with which you want to receive the encrypted messages, for example.

To verify a session immediately, send a message directly to a room:

```plain
matrix-commander --room 'REPLACE-ME' -m 'First encrypted message :)'
```

Therefore:

```plain
matrix-commander --verify emoji
```

**If you do not perform this step, the messages will be sent encrypted, but the session will not be verified and a warning will be displayed along with the message in messenger.**

### Uninstall

```bash
pip uninstall matrix-notify
```

## Bugs, Suggestions, Feedback, and Needed Support

> If you have any bugs, suggestions or feedback, feel free to create an issue or create a pull request with your changes.

## Support Me

If you like `matrix-notify`, you think it is useful and saves you a lot of work and nerves and lets you sleep better, please give it a star and consider donating.

<a href="https://www.paypal.com/donate/?hosted_button_id=4G9X8TDNYYNKG" target="_blank">
  <!--
    https://github.com/stefan-niedermann/paypal-donate-button
  -->
  <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" style="height: 90px; width: 217px;" alt="Donate with PayPal"/>
</a>