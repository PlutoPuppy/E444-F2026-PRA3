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


## Screenshots

<img width="508" height="282" alt="Screenshot 2026-09-28 at 4 36 43 PM" src="https://github.com/user-attachments/assets/b6c3e603-da7e-4785-b45d-5f0bb28cce80" />

<img width="642" height="501" alt="Screenshot 2026-09-28 at 4 59 04 PM" src="https://github.com/user-attachments/assets/1bbed8c0-47aa-4730-8b7e-629127aa6181" />

<img width="614" height="451" alt="Screenshot 2026-09-28 at 4 59 21 PM" src="https://github.com/user-attachments/assets/e725737f-4c48-4287-8fab-7712b7573bf9" />

<img width="649" height="551" alt="Screenshot 2026-09-28 at 4 59 34 PM" src="https://github.com/user-attachments/assets/0c141c06-9d2b-47d3-9460-7296a9040c19" />
