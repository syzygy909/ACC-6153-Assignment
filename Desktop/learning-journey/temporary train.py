''' ###
sentence = input('请输入一段话: ')
counter = {}
for ch in sentence:
    if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
        counter[ch] = counter.get(ch, 0) + 1
sorted_keys = sorted(counter)

print(sorted_keys)
for x in sorted_keys:
    print(f'{x} 出现了 {counter[x]} 次.')
'''

