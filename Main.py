# Alex Silence
# CS021-B
# A program that takes random wikipedia articles and compares their character count vs views in the past 60 days
# Uses BeautifulSoup, requests, matplotlib, and numpy

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot
import numpy as np


# returns the number of characters in the webpage
def get_char_num(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')

    tbody = html.find_all('tbody', class_='stat-list--group')

    try:
        tbody = str(tbody[2])

        # format to make usable
        tbody = tbody.replace('<td>', '')
        tbody = tbody.replace('</td>', '')
        tbody = tbody.replace(',','')
        tbody = tbody.splitlines()[6]

        print("Character Count: ", tbody)

        return int(tbody)
    except IndexError:
        return 0


# returns the number of views in the past 60 days
def get_popularity(url):
    page = requests.get(url).text
    html = BeautifulSoup(page, 'html.parser')

    # find num
    num = [a for a in html.select('a')
           if a['href'].find('latest-60') > -1]

    # check to make sure num was found
    if len(num) > 0:
        text = num[0].text.replace(',','')
        print("Views in the past 60 days: ", text)
        return int(text)


# gets a user defined number of points
def get_points():
    valid = False
    while not valid:
        try:
            max = int(input("Number of data points: "))
            valid = True
        except ValueError:
            print("Error, must be an int > 0")

    points = []
    for i in range(max):
        print("Link no. ", i + 1)
        link = get_random_stats_page()
        chars = get_char_num(link)
        clicks = get_popularity(link)

        # check to make sure that chars and clicks are not empty
        if chars is not None and clicks is not None:
            points.append([chars, clicks])

        i += 1
        print()

    return points


# gets a random wikipedia article
def get_random_stats_page():
    link_start = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/'
    start = 'https://en.wikipedia.org/wiki/Special:Random'
    page = requests.get(start).text
    html = BeautifulSoup(page, 'html.parser')

    # finds article title
    raw_link = html.find_all('link', rel='canonical')
    print(raw_link)

    # format to make usable
    raw_link = str(raw_link[0])
    raw_link = raw_link.lstrip('"<link href="https://en.wikipedia.org/wiki/"')
    index = raw_link.find('"')
    raw_link = raw_link[0:index]
    print(raw_link)

    return link_start + raw_link


# writes the data to a file
def write_to_file(points):
    points_file = open("points.txt", 'a')
    for i in range(len(points)):
        line = str(points[i][0]) + " " + str(points[i][1]) + "\n"
        points_file.write(line)


# uses matplotlib to create a scatterplot of points saved to the file
def create_plot():
    x = []
    y = []

    try:
        # add points
        points_file = open('points.txt', 'r')
        for line in points_file:
            x.append(float(line[0:line.find(" ")]))
            y.append(float(line[line.find(" "):line.find("\n")]))

        # create plot
        matplotlib.pyplot.scatter(x,y)

        # set axis
        matplotlib.pyplot.xlim(0, max(x))
        matplotlib.pyplot.ylim(0, max(y))

        # label axis
        matplotlib.pyplot.xlabel("Character count")
        matplotlib.pyplot.ylabel("Views in the past 60 days")

        # best fit line
        matplotlib.pyplot.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))

        # display graph
        matplotlib.pyplot.show()
    except IOError:
        print("Error creating graph")


# main program logic
def main():
    print("Welcome to my wikipedia webscraper app")
    print("Type s to add more pages data to the points text file")
    print("Type g to show the graph of the points")
    print("Type q to quit the program")

    next = input("(s/g/q): ")
    while next is not "q":
        if next == 's':
            points = get_points()
            for i in range(len(points)):
                print(points[i])
            write_to_file(points)
        if next == 'g':
            create_plot()
        next = input("(s/g/q): ")


main()
