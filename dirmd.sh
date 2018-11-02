for file in $(ls $1); do
  echo "![](/$1/$file)"
  echo
done
