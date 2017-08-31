BLOGPATH="$HOME/Dropbox/blogs/ryanmoco";
CONTENTPATH="$BLOGPATH/content";

TODAY=`date '+%Y-%m-%d'`;

POSTPATH="$CONTENTPATH/posts/Tech/${TODAY}";

mkdir -p "$POSTPATH";

touch "${POSTPATH}/${TODAY}_post.md";

open "${POSTPATH}/${TODAY}_post.md";

