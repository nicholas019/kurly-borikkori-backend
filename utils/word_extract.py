from konlpy.tag import Twitter      
from collections import Counter

def word_extract(word):
    nlpy = Twitter()
    nouns = nlpy.nouns(word)
    
    count = Counter(nouns)
    tag_count = []
    tags = []
    for n, c in count.most_common(100):
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2 and len(tags) <= 49:
            tag_count.append(dics)
            tags.append(dics['tag'])

    return tags


