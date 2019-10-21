pip3 install requests yaml
python3 codenames.py
git add codenames.json && git -c "user.name=XiaomiFirmwareUpdater" -c "user.email=xiaomifirmwareupdater@gmail.com" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$XFU@github.com/XiaomiFirmwareUpdater/xiaomi_devices.git HEAD:codenames
 
