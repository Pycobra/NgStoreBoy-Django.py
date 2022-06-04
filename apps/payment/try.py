on=True
letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'
         , 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'
         , 'y', 'z']
letters_case=[]
result=[]
cnt=0
while on:
    entry=input('write the name:')
    letters_case.append(entry)
    print(letters_case)
for words in letters_case:
    for i in words:
        cnt += 1
        if words[0] == 'a':
            if i == 'b':
                result.append(words)
