
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

