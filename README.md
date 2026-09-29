# E444-F2026-PRA3
this repo is a clone of https://github.com/miguelgrinberg/flasky

## Activity 1.4: Chapter 4 forms

Reproduces Example 4-7 with a name form, session storage, redirects after
submissions with a valid name and CSRF token, and dismissible flashed messages when the name changes.
The email field uses basic string checks without an email-validator dependency:

- Missing `@`: `Missing @ in email address`
- Contains `@` but not `utoronto` (case-insensitive): `Need to enter UofT email`
- Passes both checks: displays the submitted name and email address.

### Run

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app hello run --port 5001
```

Open http://127.0.0.1:5001. The default secret key is for local lab use;
set `SECRET_KEY` in the environment for deployment.

### Verification

The Flask test client verified these submissions with CSRF enabled:

| Name | Email input | Result |
| --- | --- | --- |
| Yixin | UofT email containing `@` and `utoronto` | Displays name and email |
| Yixin Zha | Yixin | Missing @ in email address |
| Yixin Zha | Non-UofT email containing `@` | Need to enter UofT email |

Browser verification and the Activity 1.4 screenshot are pending.

## Activity 2.4: Build and run with Docker

Run these commands from the repository root with Docker Desktop running:

```sh
docker build -t ece444-lab3 .
docker run -d --name ece444-lab3 -p 127.0.0.1:5002:5000 ece444-lab3
```

Open http://localhost:5002. The container runs the lab's Flask development server
on port 5000; host port 5002 avoids conflicts with the local Flask app.
Dependencies are installed from the root `requirements.txt`.

```sh
docker logs ece444-lab3
docker stop ece444-lab3
docker start ece444-lab3
```

## Activity 2.5: Chatbot with session memory

Submitting a name and valid UofT email opens `/chat`. Enter `My name is Alice.`
and click **Send**, then send `What is my name?`. The replies are
`Nice to meet you, Alice!` and `Your name is Alice.`

The chatbot stores the conversational name in Flask's `session['chat_name']`,
separately from the name submitted on the Home page. Memory survives requests
and page reloads in the same browser session. The displayed conversation is
kept on the page only and resets on reload.

Click **Logout** to clear the entire session and return Home. Submit the name
and UofT email again, then ask `What is my name?`. The chatbot replies
`You haven't told me your name yet.`

Run the automated checks (including logout, session isolation, and CSRF):

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Build and run the chatbot version separately:

```sh
docker build -t ece444-lab3:chat .
docker run -d --name ece444-lab3-chat -p 127.0.0.1:5003:5000 ece444-lab3:chat
```

Open http://localhost:5003.
