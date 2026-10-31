# Load Test Student Data

This directory is used to store synthetic student credentials for
local performance testing.

## Generating Test Accounts

From the backend directory, run:

python manage.py create_load_test_students --count 500 --confirm

This command:
- Creates up to 500 synthetic student accounts.
- Assigns each account the STUDENT role.
- Generates random passwords.
- Saves the credentials in students.csv.

## Security

- students.csv contains generated passwords.
- Never commit students.csv to Git.
- The credentials are excluded through the root .gitignore.
- These accounts are intended only for local testing.
- Do not use real student credentials.