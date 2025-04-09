DROP TABLE IF EXISTS MaxObservations;

DROP TABLE IF EXISTS SpeciesCounts;

-- Get data out of ABMI into SQL, subsitute TMTT for -1 to later be replaced...
UPDATE Abmi
SET
    observations = -1
WHERE
    observations = 'TMTT';

CREATE TABLE MaxObservations (species_name varchar(255), max_observations int);

-- Update what was TMTT to Max + 1 counts for that species
INSERT INTO
    MaxObservations
SELECT
    species_scientific_name,
    MAX(observations) as max_observations
FROM
    Abmi
GROUP BY
    species_scientific_name;

UPDATE Abmi
SET
    observations = (
        SELECT
            max_observations
        FROM
            MaxObservations
        WHERE
            MaxObservations.species_name = Abmi.species_scientific_name
    )
WHERE
    observations = -1;

-- Sum all observation counts based on site and species
CREATE TABLE SpeciesCounts (
    location_id varchar(255),
    year int,
    species_scientific_name varchar(255),
    counts float
);

INSERT INTO
    SpeciesCounts
SELECT
    location_id,
    year,
    species_scientific_name,
    SUM(observations) AS counts
FROM
    Abmi
GROUP BY
    location_id,
    species_scientific_name,
    year
HAVING
    SUM(observations) >= 1 AND species_scientific_name IN("SPECIES 1", "SPECIES 2", "SPECIES 3");