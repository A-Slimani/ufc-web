# extensions.py
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

template_list = sorted([f for f in os.listdir('./templates') if f.endswith('.html')])
page_list = []

for page in template_list:
    if page == 'index.html':
        title = 'Home'
        url = '/'
        page_list.insert(0, {'title': title.replace('.html', ''), 'url': url })
    else:
        page = page.replace('.html', '')
        url = f'/{page}'
        title = page.replace('-', ' ').title()
        page_list.append({'title': title, 'url': url})
