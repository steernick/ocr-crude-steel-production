# import re
#
# pattern = r'^[A-Za-z.-]+(?:\s+[A-Za-z.-]+){0,2}$'
# string = 'asadas de-rt.weqr a-sd.as'
# if re.match(pattern, string):
#     print('OK')
# else:
#     print('NO')

# set1 = set('cuba')
# set2 = set('buca')
# print(set1)
# print(set2)
# intersection = len(set1.intersection(set2))
# print(intersection)
# union = len(set1.union(set2))
# print(union)
# similarity = intersection / union
# print(similarity)


with open('input-data/all-countries-list.txt', 'r') as all_f:
    all_countries = all_f.readlines()
    all_countries = [line.strip() for line in all_countries if line.strip()]

print(all_countries)

def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


def find_similar_words_jaccard(input_word, word_list, threshold: float):
    similar_words = [word for word in word_list if jaccard_similarity(input_word, word) >= threshold]
    return similar_words


print(find_similar_words_jaccard('albnia', all_countries, 0.8))
