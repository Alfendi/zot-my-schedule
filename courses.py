import requests


class uci_schedule:
    # term, department, courseNumber (get functions)

    def __init__(self) -> None:
        self.courses = dict()

    def get_courses(self):
        url = "https://api.peterportal.org/rest/v0/schedule/soc?term=2018%20Fall&department=COMPSCI&courseNumber=161".format


response = requests.get(
    "https://api.peterportal.org/rest/v0/schedule/soc?term=2018%20Fall&department=COMPSCI&courseNumber=161")
print(response.json())
