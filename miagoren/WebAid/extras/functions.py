import datetime
import re
from ..models import Opportunity

def makeCategoryFilter(categories):
    def categoryFilter(opportunity):
        for category in categories:
            if bool(re.search(category.lower(), opportunity.categories.lower())):
                return True
        return False

    return categoryFilter

def makeLocationFilter(location):
    def locationFilter(opportunity):
        if bool(re.search(location.lower(), opportunity.location.lower())):
            return True
        return False

    return locationFilter

def makeDateFilter(date):
    l = date.split('-')
    filter_date = datetime.datetime(int(l[0]), int(l[1]), int(l[2]), tzinfo=datetime.timezone.utc)
    def dateFilter(opportunity):
        creation_time = Opportunity.objects.get(pk=opportunity.id).creation_time
        if creation_time >= filter_date:
            return True
        return False

    return dateFilter
