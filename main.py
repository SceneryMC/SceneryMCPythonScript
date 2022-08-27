import shutil

with open(r"E:\共享\torrent_hash.txt", "r") as f:
    torrents = f.readlines()
for torrent in torrents:
    torrent = torrent.strip()
    shutil.copy(rf"E:\共享\torrents\{torrent}.torrent", r"E:\共享\dst")
    shutil.copy(rf"E:\共享\torrents\{torrent}.fastresume", r"E:\共享\dst")
