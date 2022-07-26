pip3 install -r requirements.txt
python3 aer.py
git add aer.json && git -c "user.name=XiaomiFirmwareUpdater" -c "user.email=xiaomifirmwareupdater@gmail.com" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$XFU@github.com/XiaomiFirmwareUpdater/xiaomi_devices.git HEAD:aer
 
