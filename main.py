import requests
import requests.auth
import random
from flask import Flask, render_template

app = Flask(__name__)


def get_url():
    with open('passes.txt', 'r') as f:
        id = f.readline()[:-1]
        pwd = f.readline()[:-1]
        username = f.readline()[:-1]
        userpwd = f.readline()[:-1]

    client_auth = requests.auth.HTTPBasicAuth(id, pwd)
    post_data = {'grant_type': 'password', 'username': username, 'password': userpwd}
    headers = {'User-Agent': 'image retriever by ' + username}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data,
                             headers=headers)

    headers = {'Authorization': response.json()['token_type'] + ' ' + response.json()['access_token'],
               'User-Agent': 'image retriever by' + username}

    response = requests.get('https://oauth.reddit.com/r/randnsfw/top.json?t=all', headers=headers)
    lucky_number = random.randint(0, 25)
    return (response.json()['data']['children'][lucky_number]['data']['subreddit_name_prefixed'],
            response.json()['data']['children'][lucky_number]['data']['url'])


def fun():
    try:
        sub, url = get_url()
        print(url)
        if 'reddit.com' in url:
            return fun()
        if 'imgur' in url:  # TODO: fix imgur
            return fun()
        if 'gfycat' in url or 'redgifs' in url:
            return render_template('index2.html', sub=sub, url=url)
        else:
            return render_template('index.html', sub=sub, url=url)
    except IndexError:
        return fun()


@app.route("/")
def fun1():
    return fun()


@app.route("/index2.html")
def fun2():
    return fun()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
