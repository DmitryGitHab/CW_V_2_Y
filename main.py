from pprint import pprint
import requests
from tqdm import tqdm
# from alive_progress import alive_bar
import time
import yadisk


def get_token():
    list_token = []
    with open('token.txt') as file:
        for line in file:
            list_token.append(line.strip())
    return list_token


def get_response():
    url = 'https://api.vk.com/method/photos.get'
    params = {
        # 'owner_id': 1,
        'owner_id': 552934290,
        'album_id': 'profile',
        'extended': 1,
        'rev': 0,
        'v': 5.131,
        'access_token': vktoken
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


print('_______________________________________________________________________________')


class Vk_Photo:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.url = vk_response.json()['response']['items'][id]['sizes'][-1]['url']
        self.size = vk_response.json()['response']['items'][id]['sizes'][-1]['type']
        self.file_name = str(vk_response.json()['response']['items'][id]['likes']['count']) + '.txt'


def create_photo_list(numbers):
    photo_list = []
    for n in range(numbers):
        photo_name = 'photo_'+str(n)
        globals()[photo_name] = Vk_Photo(name=photo_name, id=int(n))
        photo_list.append(photo_name)
    return photo_list


def upload_all_photo(list_photo):
    ya = YaUploader(token=yatoken)
    for i in tqdm(list_photo):
        ya.upload_file_from_url(eval(i).url, eval(i).file_name)


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

    def upload_file_from_url(self, from_url, path_to):
        params = {'path': path_to, 'url': from_url}
        response = requests.post(self.url+'resources/upload', headers=self.get_headers(), params=params)
        response.raise_for_status()
        # if response.status_code == 200 or 201 or 202:
        #     print("Success")
        # pprint(response.json())
        return response.json()


if __name__ == '__main__':

    yatoken = get_token()[0].split()[-1]
    vktoken = get_token()[1].split()[-1]
    vk_response = get_response()
    # TOKEN = input('Введите ваш токен: ')
    ya = YaUploader(token=yatoken)
    # photo_list = create_photo_list(int(input('введите количтество фото')))
    photo_list = create_photo_list(5)
    upload_all_photo(photo_list)

