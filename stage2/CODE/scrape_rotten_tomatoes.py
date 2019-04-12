import requests
from bs4 import BeautifulSoup
import csv

movies_file = open('rotten_tomatoes_movies.csv', mode='w+')
movie_writer = csv.writer(movies_file, delimiter=',', quotechar='"',
                          quoting=csv.QUOTE_MINIMAL)
# add header
movie_writer.writerow(["movie_name", "movie_year", "director", "runtime",
                        "genre_list", "rating", "movie_description",
                        "certificate"])

count = 0
for year in range(1950,2020):

    url = "https://www.rottentomatoes.com/top/bestofrt/?year="+str(year)
    r = requests.get(url)
    if r.status_code != 200:
        print "request.get() failed for page{}".format(r)
        print r.status_code
        continue
    soup = BeautifulSoup(r.content,'html.parser')
    a = soup.findAll("tr",attrs={'class': None})

    for script in a[1:]:
        #temp = script.find("class=tv_show_tr tvTopListTitle")
        count = count+1
        print(count)
        #print(script)
        rating = script.find("span",attrs={'class': 'tMeterScore'}).text.strip().encode('utf-8')
        movie_name = script.find("a",attrs={'class': 'unstyled articleLink'}).text.replace('('+str(year)+')','').strip().encode('utf-8')
        movie_url = "https://www.rottentomatoes.com" +script.find("a",attrs={'class': 'unstyled articleLink'})['href']
        movie_r = requests.get(movie_url)
        if movie_r.status_code != 200:
            print "request.get() failed for page{}".format(movie_r)
            print movie_r.status_code
            continue
        movie_soup = BeautifulSoup(movie_r.content, 'html.parser')
        #print(movie_soup)
        temp = movie_soup.find_all("div",attrs={'class': 'meta-label subtle'})
        temp2 = movie_soup.find_all("div",attrs={'class': 'meta-value'})
        #print(movie_soup)
        movie_description = movie_soup.find("div",attrs={'id': 'movieSynopsis'})
        if (movie_description is not None):
            movie_description = movie_description.text.strip().encode('utf-8')
        else:
            movie_description = ""

        # print("Movie Name: " +movie_name)
        # print("Movie Description: " +movie_description)
        # print("Movie Rating: "+rating)
        # print("Movie Year: " + str(year))
        for i,attr in enumerate(temp):
            try:
                if("Directed By" in attr.text):
                    Director = temp2[i].find("a").text.strip().encode('utf-8')
                    # print("Director:"+Director)
                if ("Runtime" in attr.text):
                    Runtime = temp2[i].find("time").text.strip().encode('utf-8')
                    # print("Runtime:" + Runtime)
                if ("Rating" in attr.text):
                    Certificate = temp2[i].text.strip().encode('utf-8')
                    # print("Certificate:" + Certificate)
                if ("Genre" in attr.text):

                    genres = temp2[i].find_all("a")
                    genre_list = []
                    for genre in genres:
                        genre_list.append(genre.text.encode('utf-8'))
                    # print(",".join(genre_list))
            except:
                print("Couldn't extract a movie")
                continue
        movie_writer.writerow([movie_name, year,Director, Runtime, ",".join(genre_list), rating, movie_description,Certificate])
        print("**************")
print("Records extracted: "+str(count))
movies_file.close()




