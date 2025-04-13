-- 1
SELECT ALIVE, COUNT(*) 
FROM MarvelCharacters
GROUP BY ALIVE;

-- 2
SELECT EYE, AVG(APPEARANCES) 
FROM MarvelCharacters
GROUP BY EYE;

-- 3
SELECT HAIR, MAX(APPEARANCES) 
FROM MarvelCharacters
GROUP BY HAIR;

-- 4
SELECT IDENTIFY, MIN(APPEARANCES) 
FROM MarvelCharacters
WHERE IDENTIFY = 'Public Identity'
GROUP BY IDENTIFY;

-- 5
SELECT SEX, COUNT(*) 
FROM MarvelCharacters
GROUP BY SEX;

-- 6
SELECT IDENTIFY, AVG(Year) 
FROM MarvelCharacters
GROUP BY IDENTIFY;

-- 7
SELECT EYE, COUNT(*) 
FROM MarvelCharacters
WHERE ALIVE = 'Living Characters'
GROUP BY EYE;

-- 8
SELECT HAIR, MAX(APPEARANCES), MIN(APPEARANCES) 
FROM MarvelCharacters
GROUP BY HAIR;

-- 9
SELECT IDENTIFY, COUNT(*) 
FROM MarvelCharacters
WHERE ALIVE = 'Deceased Characters'
GROUP BY IDENTIFY;

-- 10
SELECT EYE, AVG(Year) 
FROM MarvelCharacters
GROUP BY EYE;

-- 11
SELECT name, APPEARANCES 
FROM MarvelCharacters
WHERE APPEARANCES = (SELECT MAX(APPEARANCES) FROM MarvelCharacters);

-- 12
SELECT name, Year 
FROM MarvelCharacters
WHERE Year = (
    SELECT Year 
    FROM MarvelCharacters 
    WHERE APPEARANCES = (SELECT MAX(APPEARANCES) FROM MarvelCharacters)
    LIMIT 1
);

-- 13
SELECT name, APPEARANCES 
FROM MarvelCharacters
WHERE ALIVE = 'Living Characters' 
AND APPEARANCES = (
    SELECT MIN(APPEARANCES) 
    FROM MarvelCharacters 
    WHERE ALIVE = 'Living Characters'
);

-- 14
SELECT name, HAIR, APPEARANCES 
FROM MarvelCharacters odin
WHERE APPEARANCES = (
    SELECT MAX(APPEARANCES) 
    FROM MarvelCharacters dva
    WHERE dva.HAIR = odin.HAIR
);

-- 15
SELECT name, IDENTIFY, APPEARANCES 
FROM MarvelCharacters
WHERE IDENTIFY = 'Public Identity' 
AND APPEARANCES = (
    SELECT MIN(APPEARANCES) 
    FROM MarvelCharacters 
    WHERE IDENTIFY = 'Public Identity'
);