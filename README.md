This simple Chat app was created via django. It contains a django backend and a frontend using material design. Project was expanded to multiple chatrooms and is now using websocket.

Generel js code is in the root/static/js folder.
js code specific for websockets is in the html docs in the folder root/chat/templates.

In this case, frontend and backend was not specifically separated to show the use of django in html. The base templet for all html files is in root/templates.

Documentation is made via sphinx. To start, navigate to docs and type make html.

For style, flake8 is installed. Run flake8 in CMD.

For test coverage, run
coverage run --source='.' manage.py test
coverage report
coverage html
