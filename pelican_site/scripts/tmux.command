#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

# Setup a window for tailing log files
tmux new-window -t $SESSION:1 -n 'Pelican'
tmux split-window -h
tmux select-pane -t 0
tmux send-keys "cd $HOME/dev/pelican; source bin/activate; cd $HOME/Dropbox/blogs/ryanmoco/pelican_site; fab regenerate" C-m
tmux select-pane -t 1
tmux send-keys "cd $HOME/dev/pelican; source bin/activate" C-m
tmux send-keys "cd $HOME/Dropbox/blogs/ryanmoco/pelican_site; sleep 3;fab serve" C-m

# Set default window
tmux select-window -t $SESSION:1

# Attach to session
tmux -2 attach-session -t $SESSION
