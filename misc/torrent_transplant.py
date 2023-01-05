import shutil

with open(r"E:\共享\torrent_hash.txt", "r") as f:
    torrents = f.readlines()
for torrent in torrents:
    torrent = torrent.strip()
    shutil.copy(rf"C:\Users\SceneryMC\AppData\Local\qBittorrent\BT_backup\{torrent}.torrent", r"E:\共享\dst")
    shutil.copy(rf"C:\Users\SceneryMC\AppData\Local\qBittorrent\BT_backup\{torrent}.fastresume", r"E:\共享\dst")
