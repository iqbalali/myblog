#!/bin/bash

BASE="$HOME/Dropbox (Personal)/Blogs/ryanmoco/pelican_site"

set -e
function cleanup {
  echo "Exiting..."
}
trap cleanup EXIT
source $HOME/dev/pelican/bin/activate
cd "$BASE"
fab regenerate
