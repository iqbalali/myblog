#!/bin/bash

BLOGPATH="$HOME/Dropbox/blogs/ryanmoco";
PELICNPATH="$BLOGPATH/pelican_site";

pushd "$PELICNPATH";
fab -R remote publish
popd;
