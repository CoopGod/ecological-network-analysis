DROP TABLE IF EXISTS SpearmansDistancePairs;

-- Combine spearmans data with interaction data
CREATE TABLE SpearmansDistancePairs AS
SELECT
    CASE
        WHEN species_pair IS NULL THEN pair
        ELSE species_pair
    END AS species_pair_nn,
    type,
    distance,
    ABS(spearmans) as spearmans,
    year,
    lid_count,
    p_value
FROM
    (
        SELECT
            *
        FROM
            AlbertaInteractions
            FULL OUTER JOIN (
                SELECT
                    species_pair,
                    lid_count,
                    year,
                    spearmans,
                    p_value
                FROM
                    PairSpearmans
            ) ON pair = species_pair
    )
GROUP BY
    species_pair_nn,
    year;