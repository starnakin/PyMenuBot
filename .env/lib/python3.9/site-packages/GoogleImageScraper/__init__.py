from .GoogleImageScraper import image_scraper
from .errors import QueryError, LimitError, UnpackError, DownloadError
from DynamicHtml import DynamicHtml
from os import getcwd


scraper = image_scraper()

def urls(query=None, limit=100, arguments={}):
    returnUrls = scraper.urls(query=query, limit=limit, arguments=arguments)
    return returnUrls

def download(query=None, limit=1, arguments={}):
    returnImages = scraper.download(query=query, limit=limit, arguments=arguments)
    return returnImages

def image_objects(query=None, limit=100, arguments={}):
    if not query:
        raise QueryError('"query" is a required argument')        
    elif type(query) != str and type(query) != list:
        raise QueryError('"query" argument must be a string or list.')
    
    if type(limit) != int:
        raise LimitError('"limit" argument must be an integer.')
    elif limit > 100:
        raise LimitError('"limit" argument must be less than 100.')
    
    arguments = scraper.fill_arguments(arguments)
    
    builtUrl = scraper.build_url(query, arguments)    
    searchData = scraper.get_html(builtUrl)

    try:
        imageObjects = scraper.get_images(searchData) 
    except:
        print('Failed to fetch images regularly. Trying with simulated browser.')
        searchData = DynamicHtml(builtUrl)
        try:
            imageObjects = scraper.get_images(searchData)
        except:
            raise UnpackError('Failed to fetch image objects.')
        
    return imageObjects[0:limit+1]

def download_image(url, name, path=getcwd(), download_format=None, overwrite=True):
    if download_format:
        arguments = {'download_format': download_format}
    else:
        arguments = {}
    arguments['overwrite'] = overwrite
    
    path = scraper.download_image(url, arguments, name, path)
    if path == 1:
        raise DownloadError('Failed to download image.')
    elif path == 2:
        raise FileExistsError
    return path
