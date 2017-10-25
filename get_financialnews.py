import requests
import chardet
import json
import arrow
from pyquery import PyQuery as pq
### 财经头条网
url = 'https://www.cj1.com.cn/'

def get_urls(url):
    d = requests.get(url)
    items = pq(d.text)
    urls = ['http://www.cj1.com.cn' + i.attr('href') for i in
            items('article[class="excerpt ias_excerpt"] .desc a').items()]
    return urls

def get_json(url):
    r = requests.get(url)
    # print(d.content.decode("utf-8"))
    d = r.content.decode("utf-8")
    items = pq(d)
    title = items('h1[class="single-post__title"]').text()
    content = items('section[class="article"]').text()
    data_dict = {
        'title':title,
        'content':content
    }
    date = arrow.utcnow().to('local').format('YYYY-MM-DD')
    with open('/home/richard/Documents/{}.json'.format(date), 'a+') as f:
        f.write(json.dumps(data_dict)+'\n')
def run():
    urls = get_urls(url)
    for i in urls:
        get_json(i)
if __name__ == '__main__':
    run()