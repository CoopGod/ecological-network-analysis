DROP TABLE IF EXISTS MaxObservations;

DROP TABLE IF EXISTS SpeciesCounts;

DROP TABLE IF EXISTS SpeciesPairs;

DROP TABLE IF EXISTS FilteredSpeciesPairs;

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
    SUM(observations) >= 1;

-- Transform data into pairwise species pairs
CREATE TABLE SpeciesPairs (
    species_pair varchar(255),
    lid varchar(255),
    year int,
    first_count float,
    second_count float
);

INSERT INTO
    SpeciesPairs
SELECT DISTINCT
    CASE
        WHEN s1.species_scientific_name < s2.species_scientific_name THEN CONCAT (
            s1.species_scientific_name,
            '-',
            s2.species_scientific_name
        )
        ELSE CONCAT (
            s2.species_scientific_name,
            '-',
            s1.species_scientific_name
        )
    END AS species_pair,
    s1.location_id as lid,
    s1.year,
    CASE
        WHEN s1.species_scientific_name < s2.species_scientific_name THEN s1.counts
        ELSE s2.counts
    END AS first_count,
    CASE
        WHEN s1.species_scientific_name < s2.species_scientific_name THEN s2.counts
        ELSE s1.counts
    END AS second_count
FROM
    SpeciesCounts s1,
    SpeciesCounts s2
WHERE
    s1.location_id = s2.location_id
    AND s1.year = s2.year
    AND s1.species_scientific_name != s2.species_scientific_name;

-- Output data 
CREATE TABLE FilteredSpeciesPairs AS
SELECT
    *
FROM
    SpeciesPairs
WHERE
    (species_pair, lid) IN (
        SELECT
            species_pair,
            lid
        FROM
            SpeciesPairs
        GROUP BY
            species_pair,
            lid
        HAVING
            COUNT(species_pair) >= 3
    )
ORDER BY
    species_pair,
    year;