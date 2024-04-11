pip3 install -r requirements.txt
python3 gsmarena.py
git add devices.json all/*.json && git -c "user.name=XiaomiFirmwareUpdater" -c "user.email=xiaomifirmwareupdater@gmail.com" commit -m "Sync: $(date +%d.%m.%Y) [skip ci]"
git push https://$XFU@github.com/asaldele1/xiaomi_devices.git HEAD:gsmarena 
