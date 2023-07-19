#!/bin/bash

# Start a new tmux session
tmux new-session -d -s my_session

# Split the window vertically
tmux split-window -v

# Commands to run in the first pane (Celery worker)
tmux send-keys -t my_session:0.0 'source venv/bin/activate' C-m
tmux send-keys -t my_session:0.0 'celery -A django_advertools worker -l info -P solo' C-m

# Commands to run in the second pane (Django server)
tmux send-keys -t my_session:0.1 'source venv/bin/activate' C-m
tmux send-keys -t my_session:0.1 'python manage.py runserver 0.0.0.0:8000' C-m

# Attach to the tmux session to view the output (optional)
tmux attach-session -t my_session
