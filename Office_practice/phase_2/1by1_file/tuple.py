lang = ('java', 'c++', 'python')
year = (1995, 1983, 1991)
tup = lang + year
print(f"Languages tuple: ", lang)
print(f"Languages tuple 2nd value: ", lang[1])
print(f"tuples Concatenate: ", tup)
print(f"len func of tuples: ", len(tup))
print(f"repitation of tuple 4 time: ", (tup) * 4)
print(f"slicing language [1:]: ", lang[1:])
print(f"Type of language: ", type(lang))
print(f"Small value from Language: ", min(lang))
print(f"largest value from Language: ", max(lang))
print(f"Tuple Language: ", tuple(lang))
