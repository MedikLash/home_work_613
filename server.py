from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

def valid_data(data): #Осуществляет проверку данных с горем пополам. Если передать строку в дате уронит всю программу. Требует доработки. 
    if len(data) == 4 and 1930<int(data['year'])<2020:
            result = True
    else:
        result = 'data error'
    return result

def check_data_in_db(artist):
    find_artist = album.find(artist['artist'])
    if not find_artist:
        result = valid_data(artist)
    else:
        result = 'check error'
    return result

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}: ".format(artist)
        result += ", ".join(album_names)
    return result

@route("/albums/", method="POST")
def  artist():
    user_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    resource_path = check_data_in_db(user_data)
    if resource_path == 'check error':
        message = "Переданное имя {} найдено в базе данных".format(user_data['artist'])
        result = HTTPError(409, message)
    elif resource_path == 'data error':
        message = "Неверный формат данных"
        result = HTTPError(409, message)
    else:
        user_data1 = user_data
        user_data1["year"] = int(user_data["year"])
        save_data = album.save_data(user_data1)
        result = "Данные сохранены"  
    
    return print(result)


#python -m httpie -f POST localhost:8080/albums/ year=2007 artist=MC_Vaca genre=popsa album=EPRST
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)