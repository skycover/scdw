#!/bin/sh
./manage.py syncdb
name=scdw
port=8088
if [ -z "$1" ]; then
  target=/usr/local/bin
elif [ -d "$1" ]; then
  target="$1"
else
  echo "Usage $0 'install-path' [port number]"
  exit 1
fi
if [ -n "$2" ]; then
  port=$2
fi
cat <<EOF >"$target"/$name
#!/bin/sh
port=$port
if [ -n "\$1" ]; then
  port=\$1
fi
exec `pwd`/manage.py runserver \$port
EOF
chmod +x "$target"/$name
cat <<EOF
SkyCover Duply Web is installed as $target/$name
By default it will listen on the port http://localhost:$port
EOF
