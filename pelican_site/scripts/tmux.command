#!/bin/bash
SESSION='pelicanblog'

BLOG_PATH="$HOME/Dropbox/blogs/ryanmoco/pelican_site"
CHANGEDIR="cd $BLOG_PATH"

function set_environment () {
    tmux send-keys "workon blog" C-m
    tmux send-keys "$CHANGEDIR" C-m
}

tmux -2 new-session -d -s $SESSION

# Setup a window for tailing log files
tmux new-window -t $SESSION:1 -n 'Pelican'
tmux split-window -h
tmux split-window -h
tmux select-pane -t 0
    set_environment
tmux send-keys "fab regenerate" C-m
tmux select-pane -t 1
    set_environment
tmux send-keys "sleep 3; fab serve" C-m
tmux select-pane -t 2
    set_environment
tmux send-keys "sleep 4;npm run gulp" C-m

tmux select-layout even-vertical

# Set default window
tmux select-window -t $SESSION:1

# Attach to session
tmux -2 attach-session -t $SESSION
