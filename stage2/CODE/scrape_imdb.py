#!/usr/bin/env python2.7

import csv
import requests

from bs4 import BeautifulSoup

num_pages = 100
count = 0
movies_file = open('imdb_movies.csv', mode='w+')
movie_writer = csv.writer(movies_file, delimiter=',', quotechar='"',
                          quoting=csv.QUOTE_MINIMAL)
# add header
movie_writer.writerow(["movie_name", "movie_year", "director", "runtime",
                        "genre", "rating", "description", "certificate"])

for page in xrange(1, num_pages+1):
    print "Scraping page: " + str(page)
    # url = 'https://www.imdb.com/list/ls009120901/?sort=list_order,asc&st_dt=&mode=detail&page={}'.format(page)
    url = 'https://www.imdb.com/list/ls057823854/?st_dt=&mode=detail&page={}&ref_=ttls_vm_dtl&sort=list_order,asc'.format(page)
    page = requests.get(url)
    if page.status_code != 200:
        print "request.get() failed for page{}".format(page)
        print page.status_code
        continue
    soup = BeautifulSoup(page.text, 'html.parser')
    list_item_contents = soup.find_all(class_='lister-item-content')

    for entry in list_item_contents:
        # Parse first header
        header1 = entry.find(class_='lister-item-header')
        movie_name = header1.find('a', href=True)
        movie_year = entry.find(class_='lister-item-year')
        
        # Parse second header
        runtime = entry.find(class_='runtime')
        genre = entry.find(class_='genre')
        certificate = entry.find(class_='certificate')
        
        # Parse third header
        rating = entry.find(class_='ipl-rating-star__rating')

        director_text = entry.find_all(class_='text-muted text-small')

        # Parse third row
        description = entry.find_all('p')
        
        try:
            movie_name = str(movie_name.string)
            movie_year = int(movie_year.string.strip("(I) ").strip('(').strip(')'))
            runtime = str(runtime.string)
            certificate = str(certificate.string)
            genre = str(genre.string.strip("\n").strip(" "))
            rating = float(rating.string)
            description = str(description[1].get_text().strip("\n").strip(" "))
            director = str(director_text[1].find('a', href=True).string)
            movie_writer.writerow([movie_name, movie_year, director, runtime,
                                   genre, rating, description, certificate])
            count += 1
        except:
            print "Couldn't extract ", movie_name
            continue
    print "Total extracted: " + str(count)
    print "-"*100
movies_file.close()
