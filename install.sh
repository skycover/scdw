#!/bin/sh
set -e
name=scdw
prefix=/usr/local
port=8088
target=/usr/local/bin
usage() {
  echo "Usage $0 [-b /path/to/scdw-binary (/usr/local/bin)] [-p port-number (8088)] [-d /path/to/scdw-directory (/usr/local)]"
  exit 1
}
while [ -n "$1" ]; do
  case "$1" in
    "-b")
      test -n "$2" || usage
      target="$2"
      shift 2
    ;;
    "-p")
      test -n "$2" || usage
      port="$2"
      shift 2
    ;;
    "-d")
      test -n "$2" || usage
      prefix="$2"
      shift 2
    ;;
    *)
      usage
    ;;
  esac
done
mkdir -p $target
dstdir=$prefix/$name
mkdir -p $dstdir
cp -r * $dstdir
cd $dstdir
./manage.py migrate
./manage.py createsuperuser
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
SkyCover Duply Web binary is installed as $target/$name
By default it will listen on the port http://localhost:$port
EOF
