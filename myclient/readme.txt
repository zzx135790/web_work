1. Setup
--------
- Ensure Python 3.10 is installed.
- Install the requests library:
  pip install requests
- Run the client:
  cd myclient
  python client.py
- The base_url in client.py should set to the local or server address

2. Commands
-----------
- register
  Purpose: Register a new user.
  Syntax: register
  Prompts for username, email, password.
  Example: register
           Username: student1
           Email: student1@leeds.ac.uk
           Password: secure123

- login
  Purpose: Log in to the service.
  Syntax: login
  Prompts for username, password.
  Example: login
           Username: student1
           Password: secure123

- logout
  Purpose: Log out from the service.
  Syntax: logout
  Example: logout

- list
  Purpose: List all module instances and their professors.
  Syntax: list
  Example: list
           (Displays a table of module instances)

- view
  Purpose: View average ratings of all professors.
  Syntax: view
  Example: view
           (Displays ratings as stars)

- average <professor_id> <module_code>
  Purpose: View a professor's average rating in a module.
  Syntax: average <professor_id> <module_code>
  Example: average J1 M1

- rate <professor_id> <module_code> <year> <semester> <rating>
  You have to login first
  Purpose: Rate a professor in a module instance.
  Syntax: rate <professor_id> <module_code> <year> <semester> <rating>
  Example: rate J1 M1 2020 2 4
  Note: Requires login.

- exit
  Purpose: Quit the client.
  Syntax: exit
  Example: exit

3. Server Information
---------------------
- Pythonanywhere Domain: sc15xyz.pythonanywhere.com (replace with your domain)
- Admin Site: http://sc15xyz.pythonanywhere.com/admin/
- Admin Username: zzx
- Admin Password: zzx

4. Notes
--------
- Ensure the server has sample data (add via admin site).
- Log in before using the 'rate' command.