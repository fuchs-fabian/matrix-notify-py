# matrix-notify-py

Simple Python script for sending HTML messages to a [Matrix](https://matrix.org/) room, optionally with E2E.

It took some time to find a good solution for sending encrypted messages to Matrix in a simple and uncomplicated way. I have therefore endeavoured to document everything as well as possible.

If you have any suggestions for improvement or ideas, I would be very grateful if you would simply create an issue or open a PR with your proposed solution.

You are welcome to use this template and adapt it to your needs.

To get it:

```bash
wget https://raw.githubusercontent.com/fuchs-fabian/matrix-notify-py/main/matrix.py
```

Make the script executable if required:

```bash
chmod +x ./matrix.py
```

## Preparations

> Create a special (bot) user / account! Don't use your main account!

Installing required packages:

```bash
pip install requests matrix-commander
```

## Without E2E

```python
USE_E2E = False
```

Sending **unencrypted** messages to an **encrypted**/**unencrypted** room.

![Example without E2E](/images/example_without_e2e.png)

### Requirements

|                | example / additional information                                                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| homeserver url | E.g. for a standard Matrix user `https://matrix-client.matrix.org` (available in _account_ settings)                                                                                                                      |
| access token   | To get it in [Element](https://element.io/), log in as the created user, tap on the profile picture on the top left, and go to `All settings` → `Help & About`. There should be a dropdown menu on the bottom (`Access Token`) |
| room id        | **You have to join** with this special account to **this room** before! (available in _room_ settings)                                                                                                                    |

### Usage

The following must be adjusted in the code:

```python
MATRIX_ACCESS_TOKEN = ""
MATRIX_ROOM_ID = ""
```

If necessary also:

```python
MATRIX_HOMESERVER_URL = "https://matrix-client.matrix.org"
```

## With E2E

```python
USE_E2E = True
```

Sending **encryptet** messages to an **encrypted** room.

![Example with E2E](/images/example_with_e2e.png)

> No 100% guarantee that it will work straight away.

### Requirements

- Python 3.10+
- [`matrix-commander`](https://github.com/8go/matrix-commander/tree/master)

|         | example / additional information                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------ |
| room id | **You have to join** with this special account to **this room** before! (available in _room_ settings) |

If you want to use E2E without carrying out the following steps, you will receive the following error messages:

```
ERROR: matrix-commander: E153: Credentials file was not found. Provide credentials file or use --login to create a credentials file.
INFO: matrix-commander: 1 error and 0 warnings occurred.
Failed to send message (with E2E). Error: Command '['matrix-commander', '--room', '!xyz:matrix.org', '-m', '<b>Hello World!</b>', '--html']' returned non-zero exit status 1.
```

#### `matrix-commander` parameters

| parameter      | description                         | example                          |
| -------------- | ----------------------------------- | -------------------------------- |
| `device`       | name for the sending device         | matrix-commander-notifier        |
| `user-login`   | your username                       | @test:matrix.org                 |
| `password`     | login password for your bot account |                                  |
| `homeserver`   | homeserver of your bot account      | https://matrix-client.matrix.org |
| `room-default` | room id                             | !xyz:matrix.org                  |

#### Installation

A credentials file must be created for the `matrix-commander`. To do this, execute the following:

```bash
matrix-commander --login PASSWORD --device 'REPLACE-ME' --user-login 'REPLACE-ME' --password 'REPLACE-ME' --homeserver 'REPLACE-ME' --room-default 'REPLACE-ME'
```

> You have to replace all `REPLACE-ME` with your own credentials!

To verify a room session, once you have been invited and accepted into the room, you will need to go to the bot account in the room settings with the account you want to receive the encrypted messages with and verify the current session using emojis.

In this case, it is better to start from an [Element](https://element.io/) room of the account with which you want to receive the encrypted messages, for example.

To verify a session immediately, send a message directly to a room:

```bash
matrix-commander --room 'REPLACE-ME' -m 'First encrypted message :)'
```

Therefore:

```bash
matrix-commander --verify emoji
```

> If you do not perform this step, the messages will be sent encrypted, but the session will not be verified and a warning will be displayed along with the message in messenger.

## Test and try with [Conda](https://docs.conda.io/en/latest/)

```bash
conda create --name matrix_env python=3.10
```

```bash
conda activate matrix_env
```

Update Python:

```bash
conda update python
```

(Upgrade Python:)

```bash
conda upgrade python
```

Run [`matrix.py`](./matrix.py):

```bash
python3 matrix.py
```

## Repository that uses this template

- [Checkmk-Matrix-Notifications](https://github.com/fuchs-fabian/Checkmk-Matrix-Notifications)
