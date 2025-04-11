
select * from MarvelCharacters;
-- 1

-- SELECT name, FIRST_APPEARANCE, APPEARANCES from MarvelCharacters
-- WHERE Year between 1990 and 1999  and HAIR = 'Bald' and ALIGN = 'Bad Characters';

-- 2
-- SELECT name, Eye, Year from MarvelCharacters
-- where Year is not NULL and eye is not 'Blue Eyes' and eye is not 'Green Eyes' and eye is not 'Brown Eyes' and identify = 'Secret Identity';

-- 3
-- SELECT name, Hair from MarvelCharacters
-- where hair = 'Variable Hair';

-- 4
-- SELECT name, EYE from MarvelCharacters
-- where sex = 'Female Characters' and (eye = 'Gold Eyes' or eye = 'Amber Eyes');

-- 5
-- SELECT name, FIRST_APPEARANCE from MarvelCharacters
-- where identify = 'No Dual Identity' order by Year desc;

-- 6
-- SELECT name, ALIGN, HAIR from MarvelCharacters
-- where (hair is not 'Brown Hair' and hair is not 'Black Hair' and hair is not 'Red Hair' and hair is not 'Blond Hair') and (align = 'Good Characters' or align = 'Bad Characters');

-- 7
-- select name, year from MarvelCharacters
-- where year BETWEEN 1960 and 1969;

-- 8
-- SELECT name, hair, eye from MarvelCharacters
-- where eye = 'Yellow Eyes' and hair = 'Red Hair';

-- 9
-- SELECT name, appearances from MarvelCharacters
-- WHERE APPEARANCES < 10;

-- 10
SELECT name, appearances from MarvelCharacters
order by APPEARANCES desc limit 5;