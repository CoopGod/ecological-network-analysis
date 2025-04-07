DROP TABLE IF EXISTS AlbertaInteractions;

-- Extract all possible species pairs (regardless of distance) that could take place in the Boreal Alberta
CREATE TABLE AlbertaInteractions (
    pair varchar(255),
    'type' varchar(255),
    distance int
);

INSERT INTO
    AlbertaInteractions (pair)
SELECT
    CASE
        WHEN upper(species_1) < upper(species_2) THEN CONCAT (upper(species_1), '-', upper(species_2))
        ELSE CONCAT (upper(species_2), '-', upper(species_1))
    END AS pair
FROM
    (
        SELECT
            upper(a.Latin_Name) as species_1,
            upper(b.Latin_Name) as species_2
        FROM
            (
                SELECT
                    Latin_Name
                FROM
                    BorealAlberta
                where
                    Boreal = 1
                    or Boreal = 3
            ) as a
            JOIN (
                SELECT
                    Latin_Name
                FROM
                    BorealAlberta
                where
                    Boreal = 1
                    or Boreal = 3
            ) as b ON a.Latin_Name < b.Latin_Name
    );

-- Clean up 0 distance interactions from master list for faster querying
DELETE FROM Interactions
WHERE
    season != 'Summer' -- excludes winter interactions
;

DELETE FROM Interactions
WHERE
    UPPER(given_species) NOT IN (
        SELECT
            upper(Latin_Name)
        FROM
            BorealAlberta
        WHERE
            Boreal = 1 -- Observed in the boreal region of Alberta
            or Boreal = 3 -- group nodes (i.e. trees, invertibrates, etc.)
    );

DELETE FROM Interactions
WHERE
    UPPER(target_species) NOT IN (
        SELECT
            upper(Latin_Name)
        FROM
            BorealAlberta
        WHERE
            Boreal = 1 -- Observed in the boreal region of Alberta
            or Boreal = 3 -- group nodes (i.e. trees, invertibrates, etc.)
    );

-- Using interaction master list, set distance for those with interactions trophic/nontrophic as 0
UPDATE AlbertaInteractions
SET
    type = 'trophic',
    distance = 0
WHERE
    pair IN (
        SELECT
            CASE
                WHEN upper(given_species) < upper(target_species) THEN CONCAT (upper(given_species), '-', upper(target_species))
                ELSE CONCAT (upper(target_species), '-', upper(given_species))
            END AS pair
        FROM
            Interactions
        WHERE
            interaction_type = 'trophic'
    );

UPDATE AlbertaInteractions
SET
    type = 'nontrophic',
    distance = 0
WHERE
    pair IN (
        SELECT
            CASE
                WHEN upper(given_species) < upper(target_species) THEN CONCAT (upper(given_species), '-', upper(target_species))
                ELSE CONCAT (upper(target_species), '-', upper(given_species))
            END AS pair
        FROM
            Interactions
        WHERE
            interaction_type = 'nontrophic'
    );