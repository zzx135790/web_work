import requests
import cmd
import json
import textwrap

class RatingClient(cmd.Cmd):
    prompt = 'rating> '
    intro = 'Professor Rating Client. Type help or ? to list commands.'
    base_url = "http://127.0.0.1:8000/"
    token = None
    username = None

    def do_register(self, arg):
        """Register a new user: register"""
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        response = requests.post(
            f"{self.base_url}/api/register/",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 201:
            print(f"User {username} registered successfully.")
        else:
            print(f"Error: {response.json()}")

    def do_login(self, arg):
        """Log in to the service: login <url>"""
        # if not arg:
        #     print("Please provide the service URL.")
        #     return
        # self.base_url = f"http://{arg}"
        username = input("Username: ")
        password = input("Password: ")
        response = requests.post(
            f"{self.base_url}/api/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            self.username = data['username']
            print(f"Logged in as {self.username}.")
        else:
            print(f"Error: {response.json()}")

    def do_logout(self, arg):
        """Log out from the service: logout"""
        if not self.token:
            print("Not logged in.")
            return
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.post(f"{self.base_url}/api/logout/", headers=headers)
        if response.status_code == 200:
            print(response.json()['message'])
            self.token = None
            self.username = None
        else:
            print(f"Error: {response.json()}")

    def do_list(self, arg):
        """List all module instances: list"""
        response = requests.get(f"{self.base_url}/api/module-instances/")
        if response.status_code == 200:
            instances = response.json()
            # Define column widths
            col_widths = {
                'Code': 6,
                'Name': 28,
                'Year': 6,
                'Semester': 10,
                'Taught by': 28
            }
            # Print header
            header = (f"| {{:<{col_widths['Code']}}} | {{:<{col_widths['Name']}}} | "
                      f"{{:<{col_widths['Year']}}} | {{:<{col_widths['Semester']}}} | "
                      f"{{:<{col_widths['Taught by']}}} |")
            print(header.format('Code', 'Name', 'Year', 'Semester', 'Taught by'))
            # Print separator
            separator = (f"|{'-' * col_widths['Code']}|{'-' * col_widths['Name']}|"
                         f"{'-' * col_widths['Year']}|{'-' * col_widths['Semester']}|"
                         f"{'-' * col_widths['Taught by']}|")
            print(separator)
            # Print rows
            for inst in instances:
                profs = ", ".join([f"{p['professor_id']}, {p['name']}" for p in inst['professors']])
                # Truncate fields for other columns
                code = inst['module_code'][:col_widths['Code']].ljust(col_widths['Code'])
                name = inst['module_name'][:col_widths['Name']].ljust(col_widths['Name'])
                year = str(inst['year'])[:col_widths['Year']].ljust(col_widths['Year'])
                semester = str(inst['semester'])[:col_widths['Semester']].ljust(col_widths['Semester'])
                # Wrap Taught by column
                wrapped_profs = textwrap.wrap(profs, width=col_widths['Taught by'], break_long_words=False)
                if not wrapped_profs:
                    wrapped_profs = ['']  # Handle empty professor list
                # Print first line with all columns
                taught_by = wrapped_profs[0].ljust(col_widths['Taught by'])
                print(header.format(code, name, year, semester, taught_by))
                # Print additional lines for Taught by
                for line in wrapped_profs[1:]:
                    taught_by = line.ljust(col_widths['Taught by'])
                    print(f"| {' ' * col_widths['Code']} | {' ' * col_widths['Name']} | "
                          f"{' ' * col_widths['Year']} | {' ' * col_widths['Semester']} | {taught_by} |")
        else:
            print(f"Error: {response.json()}")

    def do_view(self, arg):
        """View ratings of all professors: view"""
        response = requests.get(f"{self.base_url}/api/professors/")
        if response.status_code == 200:
            professors = response.json()
            for prof in professors:
                if prof['average_rating'] is None:
                    rating_display = "No ratings"
                else:
                    rating_display = "*" * prof['average_rating']
                print(f"The rating of {prof['name']} ({prof['professor_id']}) is {rating_display}")
        else:
            print(f"Error: {response.json()}")

    def do_average(self, arg):
        """View average rating of a professor in a module: average <professor_id> <module_code>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: average <professor_id> <module_code>")
            return
        professor_id, module_code = args
        response = requests.get(
            f"{self.base_url}/api/average/",
            params={"professor_id": professor_id, "module_code": module_code}
        )
        if response.status_code == 200:
            data = response.json()
            stars = "*" * (data['average_rating'] or 0)
            print(f"The rating of {professor_id} in module {module_code} is {stars}")
        else:
            print(f"Error: {response.json()}")

    def do_rate(self, arg):
        """Rate a professor: rate <professor_id> <module_code> <year> <semester> <rating>"""
        if not self.token:
            print("Please log in first.")
            return
        args = arg.split()
        if len(args) != 5:
            print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
            return
        professor_id, module_code, year, semester, rating = args
        try:
            year = int(year)
            semester = int(semester)
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            if not (1 <= semester <= 2):
                raise ValueError("Semester must be 1 or 2.")
        except ValueError as e:
            print(f"Error: {e}")
            return
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.post(
            f"{self.base_url}/api/ratings/",
            json={
                "professor_id": professor_id,
                "module_code": module_code,
                "year": year,
                "semester": semester,
                "rating": rating
            },
            headers=headers
        )
        if response.status_code == 201:
            data = response.json()
            print(f"Rating submitted: {data['rating']} for {professor_id} in {module_code} ({year}, Sem {semester})")
        else:
            print(f"Error: {response.json()}")

    def do_exit(self, arg):
        """Exit the client: exit"""
        return True

if __name__ == '__main__':
    RatingClient().cmdloop()