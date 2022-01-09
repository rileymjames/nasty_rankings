SET CLIENT_ENCODING = 'UTF8';
SET DATESTYLE TO ISO;
SET XML OPTION CONTENT;


DROP TABLE IF EXISTS player_data CASCADE;
DROP INDEX IF EXISTS player_data_index CASCADE;

CREATE TABLE player_data (
    pitcher         VARCHAR(25) PRIMARY KEY,
    player_name     VARCHAR(25),

CONSTRAINT pitcher_fk
    FOREIGN KEY pitcher
        REFERENCES pitch_data(pitcher)
        ON DELETE RESTRICT
);
COMMENT ON TABLE player_data IS 'Stores player data.';
CREATE INDEX player_data_index ON player_data (pitcher);
