
from marvel import full_dict

# 1(2)

def intOrNone(x):
    try:
        return int(x)
    except ValueError:
        return None

num_list = list(map(intOrNone, input('Введите числа через пробел: ').split()))

print(num_list)

# 2(3)
full_list = []

for index, film in full_dict.items():
    full_list.append(
        {
            'id': index,
            **film, 
        }
    )


idsearchlist = list(filter(lambda film: film['id'] in num_list, full_list))

print(idsearchlist)

# 3(4)

directors = {film['director'] for film in full_list}

print(directors)

# 4(6)

films_starting_with_ch = list(filter(lambda film: film['title'] and film['title'].startswith('Ч'), full_list))
print(films_starting_with_ch)

# 5(7)

# Только фильмы, вышедшие раньше 2017 года.
new_full_list = list(filter(lambda film: isinstance(film['year'], int) and film['year'] < 2017, full_list))

print(new_full_list)


# 6(8)
# Только фильмы, вышедшие раньше 2010 года и относящиеся к первой фазе.
new_full_list1 = list(filter(lambda film: film['stage']=='Первая фаза' and isinstance(film['year'], int) and film['year'] < 2010, full_list))

print(new_full_list1)

# 7(10,11)
from pprint import pprint


full_list_sorted = sorted(filter(lambda film: film['title'] and 'Тор' in film['title'], full_list), key=lambda film: film["title"] if film["title"] else "")

pprint(full_list_sorted, sort_dicts=False)
print('\n full_list отсортирован по алфавиту(названия) и отфильтрован на предмет наличия слова "Тор" в названии\n')

