import json
import requests
from tqdm import tqdm
from tqdm import tqdm_gui


def get_token():
    list_token = []
    with open('token.txt') as file:
        for line in file:
            list_token.append(line.strip())
    return list_token


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


class VkPhoto:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.url = vk_response.json()['response']['items'][id]['sizes'][-1]['url']
        self.size = vk_response.json()['response']['items'][id]['sizes'][-1]['type']
        self.file_name = str(vk_response.json()['response']['items'][id]['likes']['count']) + '.jpg'


def create_photo_list(numbers):
    photo_list = []
    for n in range(numbers):
        photo_name = 'photo_'+str(n)
        globals()[photo_name] = VkPhoto(name=photo_name, id=int(n))
        photo_list.append(photo_name)
    return photo_list


def upload_all_photo(list_photo, id):
    ya = YaUploader(token=yatoken)
    data = []
    for i in tqdm(list_photo):
        data.append({"file_name": eval(i).file_name, "size": eval(i).size})
    # for i in tqdm_gui(list_photo):   # вариант прогресс бара
        ya.upload_file_from_url(eval(i).url, eval(i).file_name, id)
    with open('text.json', 'w') as file:
        json.dump(data, file, indent=0)
    print("Задача успешно завершена!")


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


if __name__ == '__main__':
    yatoken = get_token()[0].split()[-1]  # Ya - токен. допускается раскоммитить переменную ниже, для ручного ввода
    vktoken = get_token()[1].split()[-1]
    persone_id = 1  # id Павла Дурова. допускается раскоммитить переменную ниже, для ручного ввода id персоны
    photo_count = 5  # количество фото для загрузки. допускается раскоммитить переменную, для ручного ввода кол-ва фото
    # photo_count = int(input('введите количество фото: '))
    # persone_id = int(input('введите id персоны: '))
    # yatoken = input('Введите ваш Yandex - токен: ')
    vk_response = get_response(persone_id)
    ya = YaUploader(token=yatoken)
    ya.create_folder(persone_id)
    photo_list = create_photo_list(photo_count)
    upload_all_photo(photo_list, persone_id)
