#!/bin/bash

venv_home=$HOME/dev/pelican/
blog_home="$HOME/Dropbox/Blogs/ryanmoco/pelican_site"
log_dir="$HOME/Dropbox/Scripts/logs/blog_publish.log"

cd "$blog_home"
source "$venv_home/bin/activate"
echo "$(/bin/date '+%Y/%m/%d %H:%M:%S') -- Publishing blog" >> "$log_dir"
fab publish -R remote >> "$log_dir"
echo "$(/bin/date '+%Y/%m/%d %H:%M:%S') -- Done" >> "$log_dir"
