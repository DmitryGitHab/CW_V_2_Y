import json
import requests
import datetime
from tqdm import tqdm
from tqdm import tqdm_gui

""" TODO:
 readme
"""

def get_token():
    list_token = []
    with open('token.txt') as file:
        for line in file:
            list_token.append(line.strip())
    return list_token


def create_photo_list(numbers, social_network):
    photo_list = []
    for n in range(numbers):
        photo_name = 'photo_'+str(n)
        globals()[photo_name] = social_network(name=photo_name, id=int(n))
        photo_list.append(photo_name)
    return photo_list


def write_json(data):
    with open('text.json', 'w') as file:
        json.dump(data, file, indent=0)
    print("JSON данные записаны в файл")


class VkPhoto:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.url = vk_response.json()['response']['items'][id]['sizes'][-1]['url']
        self.size = vk_response.json()['response']['items'][id]['sizes'][-1]['type']
        self.file_name = str(vk_response.json()['response']['items'][id]['likes']['count'])
        self.upload_date = vk_response.json()['response']['items'][id]['date']

    def get_persone_id(name_id):
        persone_id = name_id
        url = "https://api.vk.com/method/utils.resolveScreenName"
        params = {
            "access_token": vktoken,
            "v": "5.131",
            "screen_name": name_id
            }
        responce = requests.get(url, params=params)
        if name_id.isdigit():
            return persone_id
        else:
            persone_id = responce.json()['response']['object_id']
            return persone_id


    def get_response(id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'rev': 0,
            'v': 5.131,
            'access_token': vktoken
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response


class YaUploader:

    def __init__(self, token):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk/'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            "Host": "cloud-api.yandex.net"
        }

    def create_folder(self, id):
        path = 'id_'+str(id)
        params = {'path': path}
        response = requests.put(self.url+'resources', headers=self.get_headers(), params=params)
        # response.raise_for_status()
        if response.status_code == 200 or 201 or 202:
            print(f'Директория "{path}", успешно создана')

    def upload_file_from_url(self, from_url, path_to, id):
        params = {'path': 'id_'+str(id)+'/'+path_to, 'url': from_url}
        response = requests.post(self.url+'resources/upload', headers=self.get_headers(), params=params)
        response.raise_for_status()
        if response.status_code == 200:
            print("Задача успешно выполнена")
        # pprint(response.json())
        # return response.json()

    def upload_all_photo(self, list_photo, id):
        data = []
        check_box = []
        for i in tqdm(list_photo):
            if str(eval(i).file_name) in check_box:
                date = datetime.date.fromtimestamp(eval(i).upload_date).strftime("%Y-%m-%d")
                data.append({"file_name": eval(i).file_name+'_'+date+'.jpg', "size": eval(i).size})
                ya.upload_file_from_url(eval(i).url, eval(i).file_name+'_'+date+'.jpg', id)
                check_box.append(eval(i).file_name)
            else:
                data.append({"file_name": eval(i).file_name+'.jpg', "size": eval(i).size})
                ya.upload_file_from_url(eval(i).url, eval(i).file_name+'.jpg', id)
                check_box.append(eval(i).file_name)
        print("Файлы успешно загружены на Яндекс-Диск!")
        write_json(data)
        return data


if __name__ == '__main__':
    yatoken = get_token()[0].split()[-1]  # Ya - токен. допускается раскоммитить переменную ниже, для ручного ввода
    vktoken = get_token()[1].split()[-1]
    profile_name = 'begemot_korovin'
    persone_id = VkPhoto.get_persone_id(profile_name)
    photo_count = 5  # количество фото для загрузки. допускается раскоммитить переменную, для ручного ввода кол-ва фото
    # photo_count = int(input('введите количество фото: '))
    # profile_name = int(input('введите id персоны: '))
    # yatoken = input('Введите ваш Yandex - токен: ')
    vk_response = VkPhoto.get_response(persone_id)
    ya = YaUploader(token=yatoken)
    ya.create_folder(persone_id)
    photo_list = create_photo_list(photo_count, VkPhoto)
    ya.upload_all_photo(photo_list, persone_id)




