from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen


def is_number(s):
    for c in s:
        if not c.isdigit() and c != '.':
            return False
    return True;



def proc_season_url(url):
    """ Process season's page """
    html = urlopen(url).read()
    soup = BeautifulSoup(html)

    # Find the relevant table in the season page
    table = soup.find('table', attrs={"class": "wikitable plainrowheaders wikiepisodetable"})

    sum_of_viewers = 0
    row_index = 0
    for table_row in table.findAll("tr"):
        if row_index > 0:
            # Exclude header row
            col_index = 0
            for table_data in table_row.findAll("td"):
                if col_index == 5:
                    # US viewers are in column 5
                    num_viewers = str(table_data.contents[0])
                    # print row_index, num_viewers  # For debugging only
                    if is_number(num_viewers):
                        sum_of_viewers += float(num_viewers)

                col_index += 1
        row_index += 1

    return sum_of_viewers


def proc_main_url(url):
    """ Process main page """
    html = urlopen(url).read()
    soup = BeautifulSoup(html)

    # Find the relevant table in the main page
    table = soup.find('table', attrs={"class": "wikitable plainrowheaders"})

    sum_of_viewers = 0
    for link in table.findAll("a"):
        if link.string.startswith('Season'):
            # print link["href"]  # For debugging only
            season_url = "https://en.wikipedia.org" + link["href"]
            sum_of_viewers += proc_season_url(season_url)

    return sum_of_viewers




url = 'https://en.wikipedia.org/wiki/Game_of_Thrones'

sum_of_viewers = proc_main_url(url)

print "Total number of US viewers: %.2f millions" % sum_of_viewers