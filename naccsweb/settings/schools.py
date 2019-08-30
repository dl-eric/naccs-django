import requests

SCHOOLS_ENDPOINT = 'http://universities.hipolabs.com/search'

# Returns a mapping of school names to school domains
def get_schools():
    ca = requests.get(SCHOOLS_ENDPOINT, params={'country':'Canada'})
    ca = ca.json()
    us = requests.get(SCHOOLS_ENDPOINT, params={'country':'United States'})
    us = us.json()

    mapping = {}

    for school in ca:
        # The API we use have duplicates for some reason... so we add domains
        # from each duplicate.
        if mapping.get(school.get('name')):
            mapping[school.get('name')] += school.get('domains')
        else:
            mapping[school.get('name')] = school.get('domains')
    
    for school in us:
        if mapping.get(school.get('name')):
            mapping[school.get('name')] += school.get('domains')
        else:
            mapping[school.get('name')] = school.get('domains')

    return mapping
