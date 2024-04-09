import os
import asyncio
import platform

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from database import create_item, get_items

from configs.credential import CONTAINER_ID

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
async def hello():
   name = request.form.get('name')
   
   # Get the total Count of Container Items
   items = await get_items(CONTAINER_ID)

   # Create the New User
   user = {
       "id": str(len(items) + 1),
       "name": name
   }

   await create_item(CONTAINER_ID, user)

   if name:
       print('Request for hello page received with name=%s' % name)

       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


def insert_name(name):
    print(name)


if __name__ == '__main__':
   app.run()
