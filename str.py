import csv

# Don't call this function
from ast import parse
from turtle import clear

filename = "strrecentcleaned.txt"


def sanitize_file():
    # Open file and read lines
    f = open(filename, "r")
    lines = f.readlines()

    # Reopen file and start writing
    f = open(filename, "w")
    # Strip *.png *.jpg and random 1s from txt file
    for line in lines:
        if not ".png" in line and not ".jpg" in line and line.strip("\n") != "1":
            f.write(line)

    f.close()

    input = open(filename, 'r')
    output = open('out.txt', 'w')
    clean = input.read().replace(":white_circle: ", "").replace(":large_blue_circle: ", "").replace(":white_check_mark:", "").replace(":red_circle: ", "").replace(":large_green_circle: ", "")
    output.write(clean)


# Dict format:
# {
#   requester:
#   company_name:
#   arr:
#   region:
#   sfdc_link:
#   current_opp:
#   provided_support:
#   urgency:
#   topic:
#   request_description:
# }

def strip_line(line):
    return line.strip("\n").strip("\xa0")

def transform_arr(line):
    transformed_arr = strip_line(line)
    transformed_arr = transformed_arr.replace('k', '000').replace('K', '000')
    return transformed_arr


def parse_file(filepath):
    """
    Parses text for dictionary items above from given filepath

    Params
    ---------
    filepath: str

    Returns
    ---------
    requests: list of dicts
    
    """

    requests = []
    request = {}
    prev_line = ""

    with open(filepath, "r") as file_object:
        for line in file_object:
            # If we see "Request a Solutions Engineer" but request dict is populated, it means a new request has started
            # so finish the request and append to requests list
            if "Request a Solutions Engineer" in line and request:
                request_copy = request.copy()
                requests.append(request_copy)
                request.clear()

            # Find Requester
            if "@" in line and "WORKFLOW" in prev_line:
                request['requester'] = strip_line(line)

            # Find Company Name
            if "has requested a Solution Engineer for" in line:
                request['company_name'] = strip_line(line.split("has requested a Solution Engineer for",1)[1])

            # Find ARR
            if "ARR" in prev_line:
                print(transform_arr(line))
                request['arr'] = transform_arr(line)

            # Find Region
            if "Region" in prev_line:
                request['region'] = strip_line(line)

            # Find SFDC Link
            if "SFDC link" in prev_line:
                request['sfdc_link'] = strip_line(line)

            # Find if request is an active Opportunity
            if "Is there an opportunity?" in prev_line:
                request['current_opp'] = strip_line(line)

            # Find if Support has been provided so far
            if "Who has provided support so far?" in prev_line:
                request['provided_support'] = strip_line(line)

            # Find Urgency
            if "Urgency:" in prev_line:
                request['urgency'] = strip_line(line)

            # Find Topic
            if "Topic:" in prev_line:
                request['topic'] = strip_line(line)

            # Find Request Description
            # if "The request:" in prev_line:


            prev_line = line
    request_copy = request.copy()
    requests.append(request_copy)
    print(requests)
    return requests


def write_to_spreadsheet(reqs):

    columns = ['requester', 'company_name', 'arr','region','sfdc_link','current_opp','provided_support','urgency', 'topic']

    with open('solutions_technical_requests.csv', 'a', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()
        for key in reqs:
            writer.writerow(key)

# parse_file(filename)

write_to_spreadsheet(parse_file(filename))