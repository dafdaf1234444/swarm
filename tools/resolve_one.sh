#!/data/data/com.termux/files/usr/bin/bash

ID=$1

echo "=== ORIENT ==="
python tools/orient.py | tail -20

echo ""
echo "=== FIND $ID ==="
grep -R "$ID" .

echo ""
echo "Decide: (k)eep / (d)elete / (s)kip"
read -t 3 action || action="s"

if [ "$action" = "d" ]; then
  echo "Edit/delete manually, then press enter"
  read
  git add .
  git commit -m "resolve $ID"
elif [ "$action" = "k" ]; then
  git commit --allow-empty -m "acknowledge $ID"
else
  echo "Skipped"
fi
