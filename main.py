with open('/home/scenerymc/.local/share/qBittorrent/BT_backup/40da8eb95d18a5e3dfe95c7d4cbf95e8a06f49b8.fastresume', 'rb') as f:
    bits = f.read()
src = bytes('/home/scenerymc/下载', encoding="utf-8")
dst = bytes('/mnt/usb-Seagate_BUP_Portable_00000000NABAY8FL-0:0-part2/收藏/音乐', encoding="utf-8")
bits = bits.replace(src, dst)
with open('/home/scenerymc/.local/share/qBittorrent/BT_backup/40da8eb95d18a5e3dfe95c7d4cbf95e8a06f49b8.fastresume', 'wb') as f:
    f.write(bits)

