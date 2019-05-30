pip3 install requests
python3 names.py
git add names.json && git -c "user.name=XiaomiFirmwareUpdater" -c "user.email=xiaomifirmwareupdater@gmail.com" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$XFU@github.com/XiaomiFirmwareUpdater/xiaomi_devices.git HEAD:names
 
