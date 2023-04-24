def match_word(word):
    if word_length != len(word):
        return False
    for i in range(word_length):
        if word[i] in nonexist_alpha \
                or known_word[i] == '_' and word[i] in exist_alpha \
                or known_word[i] != '_' and word[i] != known_word[i]:
            return False
    return True


with open("words.txt", "r") as f:
    words = f.readlines()
    while True:
        known_word = input("已知单词形式：")
        word_length = len(known_word)
        exist_alpha = list(known_word)
        while '_' in exist_alpha:
            exist_alpha.remove('_')
        nonexist_alpha = input("不存在的字母：")

        for word in words:
            word = word.strip().lower()
            if match_word(word):
                print(word)
