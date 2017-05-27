#!/bin/bash
file="$1"
cd "/Users/rjames/Dropbox/blogs/ryanmoco/pelican_site"
fab -R local publish
fab pushover
