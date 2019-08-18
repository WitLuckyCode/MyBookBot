#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import config

dKey = config.devKey['key']
bURL = config.baseURL

def findBookByTitleAuthorISBN(query):
    queryURL = bURL + "search/index.xml"
    data = {'key' : dKey, 'q' : query}
    
    try:
        response = requests.get(queryURL, params = data)
        
    except requests.exceptions.RequestException as e:
        print(e)
    #print(response)   
    soup = BeautifulSoup(response.text, "xml")
    books = {}
    count = 0
    for workTag in soup.find_all("work"):
        bookDetails = {'title' : workTag.best_book.title.string, 'bookID' : workTag.best_book.id.string
                       ,'author' : workTag.find('name').get_text(), 'authorID' : workTag.best_book.author.id.string
                       ,'image' : workTag.best_book.image_url.string, 'rating' : workTag.average_rating.string
                       ,'ratingCount' : workTag.ratings_count.string, 'oriPubYear' : workTag.original_publication_year.string
                       ,'oriPubMonth' : workTag.original_publication_month.string, 'oriPubDay' : workTag.original_publication_day.string}
        books.update({count : bookDetails})
        count += 1
        #print(count)
        #print(books)
        
    print(response.url)
    return books
    
#print(findBookByTitleAuthorISBN("philip reeve")) #test output

