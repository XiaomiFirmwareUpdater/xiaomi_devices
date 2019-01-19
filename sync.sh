pip3 install requests
curl -H "PRIVATE-TOKEN: $GITLAB_OAUTH_TOKEN_VE" 'https://gitlab.com/api/v4/projects/7746867/repository/files/lscript.py/raw?ref=master' -o lscript.py
python3 lscript.py > devices.json
git add devices.json && git -c "user.name=XiaomiFirmwareUpdater" -c "user.email=xiaomifirmwareupdater@gmail.com" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$XFU@github.com/XiaomiFirmwareUpdater/xiaomi_devices.git HEAD:master
 
