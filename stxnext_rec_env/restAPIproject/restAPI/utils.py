def find_values(dictionary : dict, book_data: dict):
    ''' fill book_data with dictionary data '''
    
    for k,v in dictionary.items():
        if k in book_data.keys():
            book_data[k] = v
        elif isinstance(v, dict):
            book_data = find_values(v, book_data)

    return book_data

def handle_book_data(item : dict):
    '''
    item - dict with json data describing book object
    extract needed data from item and return it as a dictionary
    ''' 

    # template of book's data
    book_data = {'title': None, 'publishedDate': None, 
                'authors': None, 'categories': None, 
                'averageRating': None, 'ratingsCount': None, 
                'thumbnail': None, 'year': None, 'published_date': None,
                'average_rating': None, 'ratings_count': None
                }
    # fill book_data with incoming data
    book_data = find_values(item, book_data)

    book_data['published_date'] = book_data.pop('publishedDate', None)
    book_data['average_rating'] = book_data.pop('averageRating', None)
    book_data['ratings_count'] = book_data.pop('ratingsCount', None)

    # extract year from published_date
    book_data['year'] = int(book_data['published_date'].split('-')[0])

    return book_data

def create_query_url(url: str, params: list):
    ''' return url with query parameters given in params '''
    url += '?'

    for i in params:
        url += f'{i[0]}={i[1]}&'

    return url
