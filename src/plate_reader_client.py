"""PlateReader client."""
import requests
import sys


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()

    def task2(self, img_ids: list[str]):
        res = requests.post(
            f'{self.host}/tasktwo',
            json={
                'img_ids': img_ids,
            },
        )
        return res.json()

    def task1(self, img_id: str):
        res = requests.post(
            f'{self.host}/taskone',
            json={
                'img_id': img_id,
            },
        )
        return res.json()


    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            json={
                'user': user,
            },
        )

        return res.json()


if __name__ == '__main__':
    arg = 'task2'
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    res = None
    if arg == 'task0':
        with open('./images/9965.jpg', 'rb') as im:
            res = client.read_plate_number(im)
    if arg == 'task1':
        res = client.task1('9965')
    if arg == 'task2':
        res = client.task2(['10022', '9965'])
    print(res)


