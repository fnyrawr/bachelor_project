import requests
import json
from datetime import datetime
from pprint import pp


def main():
    api_key = 'LusnxbR0.jOKczA93KtqgfcOLDoTXLIA9SNBebimq'
    url = 'http://127.0.0.1:8000/users/test'
    user = {
        "username": "test",
        "staff_id": "90001",
        "last_name": "Insert",
        "first_name": "Test",
        "email": "Test.Insert@trash-me.com",
        "is_superuser": False,
        "role": "E",
        "is_staff": False,
        "is_active": True
    }
    r = requests.delete(url, headers={'X-Api-Key': api_key}, data=user)
    print(r.status_code)
    print(r.headers)
    pp(json.loads(r.text))


if __name__ == '__main__':
    main()
