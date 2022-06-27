import json
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from os import getcwd, mkdir, listdir
from os.path import join, basename
from DynamicHtml import DynamicHtml
import requests
import imghdr
from time import sleep
from .errors import LimitError, ArgumentError, QueryError, UnpackError

class image_scraper:
        def __init__(self):
            self.path = getcwd()

        def urls(self, query=None, limit=100, arguments={}):
            arguments = self.fill_arguments(arguments)
            if not query:
                raise QueryError('"query" is a required argument')        
            elif type(query) != str and type(query) != list:
                raise QueryError('"query" argument must be a string or list.')
            
            if type(limit) != int:
                raise LimitError('"limit" argument must be an integer.')
            elif limit > 100:
                raise LimitError('"limit" argument must be less than 100.')
            
            builtUrl = self.build_url(query, arguments)
            
            try:
                searchData = self.get_html(builtUrl)
            except requests.exceptions.ConnectionError:
                sleep(3)
                try:
                    searchData = self.get_html(builtUrl)
                except requests.exceptions.ConnectionError:
                    raise UnpackError('Failed to connect to server. Check your internet and try again?')
                
            try:
                if arguments['verbose']:
                    print(f'Extracting image urls from "{builtUrl}"')
                imageObjects = self.get_images(searchData) 
            except:
                print('Failed to fetch images regularly. Trying with simulated browser.')
                searchData = DynamicHtml(builtUrl)
                try:
                    imageObjects = self.get_images(searchData)
                except:
                    raise UnpackError('Failed to fetch image objects.')
            
            if limit > len(imageObjects):
                limit = len(imageObjects)
                if 'from_download' not in arguments:
                    print(f'Failed to fetch all {limit} images. Only {len(imageObjects)} were found')
              
            urls = [imageObjects[image]['url'] for image in range(limit)]
            return urls
                
        def download(self, query=None, limit=1, arguments={}):
            arguments = self.fill_arguments(arguments)
            arguments['from_download'] = True
            urls = self.urls(query, arguments=arguments)
            
            if type(limit) != int:
                raise LimitError('"limit" argument must be an integer.')
            elif limit > 100:
                raise LimitError('"limit" argument must be less than 100.')
            
            if arguments['path']:
                path = arguments['path']
            else:
                path = self.path
                
            if arguments['directory']:
                currentPath = join(path, arguments['directory'])
            else:
                currentPath = join(path, 'images')
                
            try:
                mkdir(currentPath)
            except FileExistsError:
                pass
                
            if type(query) == str:
                    query = query.split(' ')
            prefix = 0
            images = {'images':[]}
            errors = 0
            item = 0
            for i in range(limit):
                try:
                    url = urls[item]
                    
                    name = f'{"".join(query)}-{prefix}'
                    files = listdir(currentPath)
                    nameTaken = any([name in x for x in files]) #Check if the filename is taken
                    #If the filename is taken and overwrite is False or not specified, imcrease prefix and update name until it is not taken ==>
                    while nameTaken and not arguments['overwrite']: 
                        prefix += 1
                        name = f'{"".join(query)}-{prefix}'
                        nameTaken = any([name in x for x in files]) #Check if the filename is taken
                    #Try downloading the image, and if it fails, skip to the next image ==>
                    downloadPath = self.download_image(url, arguments, name, currentPath)
                    while downloadPath == 1:
                        print('Download failed. Skipping image.')
                        item += 1
                        url = urls[item]
                        downloadPath = self.download_image(url, arguments, name, currentPath)
                
                except IndexError: #Stop downloading and update errors if there are not enough urls to supply the limit.
                    errors = limit - len(images['images'])
                    break
                
                if arguments['verbose']:
                    print(f'Downloaded "{basename(downloadPath)}" to "{downloadPath}"')
                
                images['images'].append({'path': downloadPath, 'url': url})
                prefix += 1
                item += 1
            
            images['errors'] = errors
            return images
        
        def download_image(self, url, arguments, name, path):
            arguments = self.fill_arguments(arguments)
                
            if arguments['download_format']:
                response = requests.get(url=url, stream=True)   
                try:
                    img = Image.open(BytesIO(response.content))
                    imageFormat = arguments['download_format'].lower()
                    downloadPath = join(path, f'{name}.{imageFormat}')
                    img.save(downloadPath)
                except UnidentifiedImageError:
                    return 1
            else:
                try:
                    headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
                    with requests.get(url, stream=True, timeout=5, headers=headers) as response:
                        imgFormat = imghdr.what(None, response.content)
                        if imgFormat == None and '.jpg' in url:
                            imgFormat = 'jpg'
                        elif imgFormat == None and '.jpg' not in url:
                            return 1
                        if imgFormat == 'jpeg':
                            imgFormat = 'jpg'
                        downloadPath = join(path, f'{name}.{imgFormat}')
                        with open(downloadPath, "wb") as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        return downloadPath
                except:
                    return 1

            return downloadPath
        
        def build_url(self, query, arguments={}):
            
            parameterList = ['search_format',  'color', 'color_type', 'license', 'image_type', 'time', 'aspect_ratio']
            
            parameters = {'color': {'red': 'ic:specific%2Cisc:red', 'orange': 'ic:specific%2Cisc:orange', 'yellow': 'ic:specific%2Cisc:yellow', 'green': 'ic:specific%2Cisc:green', 'teal': 'ic:specific%2Cisc:teel', 'blue': 'ic:specific%2Cisc:blue', 'purple': 'ic:specific%2Cisc:purple', 'pink': 'ic:specific%2Cisc:pink', 'white': 'ic:specific%2Cisc:white', 'gray': 'ic:specific%2Cisc:gray', 'black': 'ic:specific%2Cisc:black', 'brown': 'ic:specific%2Cisc:brown'},
                'color_type': {'color': 'ic:full', 'grayscale': 'ic:gray', 'transparent': 'ic:trans'},
                'license': {'creative_commons': 'il:cl', 'other_licenses': 'il:ol'},
                'type': {'face': 'itp:face', 'photo': 'itp:photo', 'clipart': 'itp:clipart','lineart': 'itp:lineart', 'gif': 'itp:animated'},
                'time': {'past_day': 'qdr:d', 'past_week': 'qdr:w', 'past_month': 'qdr:m','past_year':'qdr:y'},
                'aspect_ratio': {'tall': 'iar:t', 'square': 'iar:s', 'wide': 'iar:w', 'panoramic': 'iar:xw'},
                'search_format': {'jpg': 'ift:jpg', 'gif': 'ift:gif', 'png': 'ift:png', 'bmp': 'ift:bmp', 'svg': 'ift:svg', 'webp': 'webp', 'ico': 'ift:ico', 'raw': 'ift:craw'}}

            if not arguments:
                arguments = {}
            
            if not query:
                raise QueryError("'query' is a required argument")
            if type(query) == str:
                query = query.split(' ')
            joinedQuery = '%20'.join(query)
            
            builtArgs = '&tbs='
            counter = 0
            
            for param in parameterList:
                if arguments[param]:
                    try:
                        item = parameters[param][arguments[param]]
                        if counter != 0:
                            builtArgs += ','
                        builtArgs += item
                        counter += 1 
                    except NameError:
                        raise ArgumentError(f"Invalid argument for {param}! Valid arguments are {parameters[param].values}")

            baseUrl = 'https://www.google.com/search?tbm=isch&q='
            
            if counter != 0:
                return baseUrl + joinedQuery + builtArgs
            else:
                return baseUrl + joinedQuery
            
        def get_images(self, page):
            startChar = page.find('[', page.rfind('AF_initDataCallback'))
            endChar = page.find('</script>', startChar) - 20
            
            pageJson = page[startChar:endChar] 
            pageJson = json.loads(pageJson.encode('utf-8').decode('unicode_escape'))

            imageObjects = pageJson[31][0][12][2]            
            images = []
            for imageObject in imageObjects:
                if imageObject[1]:
                    image = {}
                    image['thumbnail'] = imageObject[1][2][0]
                    image['url'] = imageObject[1][3][0]
                    sourceInfo = imageObject[1][9]['2003']
                    image['source_url'] = sourceInfo[2]
                    image['source'] = sourceInfo[17]
                    images.append(image)
            return images
        
        def get_html(self, url):
            headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
            searchPage = requests.get(url=url, headers=headers)
            searchData = str(searchPage.content)
            return searchData
        
        def fill_arguments(self, arguments):
            allArguments = ['download_format', 'directory', 'path', 'color', 'color_type', 'license', 'image_type', 'time', 'aspect_ratio', 'search_format', 'verbose', 'overwrite']
            for arg in allArguments:
                if arg not in arguments:
                    arguments[arg] = None
            return arguments
            
if __name__ == '__main__':
        scraper = image_scraper()
        images = scraper.download(query='cats', limit=10, arguments={'color': 'black'})
        print(images)
