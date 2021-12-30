from pprint import pprint
import requests
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
        'owner_id': 1,
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
    for n in range(numbers):
        photo_name = 'photo_'+str(n)
        globals()[photo_name] = Vk_Photo(name=photo_name, id=int(n))


def teeeeeeeest():
    print(photo_0.name, photo_0.size, photo_0.file_name, photo_0.url)
    print(photo_1.name, photo_1.size, photo_1.file_name, photo_1.url)
    print(photo_2.name, photo_2.size, photo_2.file_name, photo_2.url)
    print(photo_3.name, photo_3.size, photo_3.file_name, photo_3.url)
    print(photo_4.name, photo_4.size, photo_4.file_name, photo_4.url)


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
        if response.status_code == 200 or 201 or 202:
            print("Success")
        pprint(response.json())
        return response.json()


if __name__ == '__main__':

    yatoken = get_token()[0].split()[-1]
    vktoken = get_token()[1].split()[-1]
    vk_response = get_response()
    create_photo_list(5)
    teeeeeeeest()
    # TOKEN = input('Введите ваш токен: ')
    # aaaa = 'https://avatars.mds.yandex.net/i?id=2a55270ec332b3b94b87cdf0e0bec1ec-5646019-images-thumbs&n=13'
    ya = YaUploader(token=yatoken)

    ya.upload_file_from_url('https://avatars.mds.yandex.net/i?id=2a55270ec332b3b94b87cdf0e0bec1ec-5646019-images-thumbs&n=13', 'cat.jpg')
    # ya.upload_file_to_disk('cat.jpg', 'https://avatars.mds.yandex.net/i?id=2a55270ec332b3b94b87cdf0e0bec1ec-5646019-images-thumbs&n=13')

    # ya.upload_file_to_disk(photo_0.name, photo_0.url)
    # ya.upload_file_to_disk(photo_1.name, photo_1.url)
    # ya.upload_file_to_disk(photo_2.name, photo_2.url)
