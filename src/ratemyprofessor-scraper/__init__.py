import requests
import json
TEACHER_QUERY = "https://www.ratemyprofessors.com/search/professors/"
QUERY_FIELD = "?q="

SCHOOL_QUERY = "https://www.ratemyprofessors.com/search/schools/"

PROF_PAGE_URL = "https://www.ratemyprofessors.com/"

DEFAULT_SCHOOL_ID = "1" # Abilene Christian University

# Might add docs here once I write more code

class RMPScraper:
    def __init__(self):
        self.school_id = DEFAULT_SCHOOL_ID
    
    def __init__(self, school_name):
        self.school_id = self.get_school_id(school_name)

    def get_school_id(self, school_name):
        r = requests.get(SCHOOL_QUERY + QUERY_FIELD + school_name)
        s = r.text
        start_index = s.find("/school/")
        if start_index == -1: # nothing found
            return DEFAULT_SCHOOL_ID
        start_index += 8
        end_index = s.find('"', start_index)
        return s[start_index:end_index]
    
    def set_school_id(self, school_id):
        self.school_id = school_id
    
    def set_school_name(self, school_name):
        self.school_id = self.get_school_id(school_name)

    def get_prof_rating(self, prof_name, keep_middle_name = False): # possible issue here: might get the wrong prof if multiple profs at a school have the same name
        if not keep_middle_name:
            prof_name = self.__remove_middle_name__(prof_name)
        r = requests.get(TEACHER_QUERY + self.school_id + QUERY_FIELD + prof_name)
        s = r.text
        index = s.find("avgRating")
        if index == -1: # nothing found
            return {"Found": False}
        index += 11

        start_index = s.rfind('{', 0, index)
        end_index = s.find('}', s.find('}', start_index) + 1)
        print(s[start_index:end_index + 1])
        result = json.loads(s[start_index:end_index + 1])
        result["Found"] = True

        return result
    # just some QOL stuff that is from the last time I tried this (middle names are inconsistent sometimes)
    def __remove_middle_name__(self, fullName):
        name = fullName.split(" ")
        newName = name[0] + " " + name[-1]
        return newName
