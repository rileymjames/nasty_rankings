SET CLIENT_ENCODING = 'UTF8';
SET DATESTYLE TO ISO;
SET XML OPTION CONTENT;


DROP TABLE IF EXISTS pitch_data CASCADE;
DROP INDEX IF EXISTS pitch_data_index CASCADE;

CREATE TABLE pitch_data (
    game_date                           DATE,
    pitch_type                          VARCHAR(25),
    batter                              VARCHAR(25),
    pitcher                             VARCHAR(25),
    release_speed                       DECIMAL,
    release_pos_x                       DECIMAL,
    release_pos_y                       DECIMAL,
    release_pos_z                       DECIMAL,
    events                              VARCHAR(25),
    description                         VARCHAR(255),
    spin_axis                           DECIMAL,
    zone                                SMALLINT,
    game_type                           VARCHAR(25),
    stand                               VARCHAR(25),
    p_throws                            VARCHAR(25),
    vx0                                 DECIMAL,
    vy0                                 DECIMAL,
    vz0                                 DECIMAL,
    ax                                  DECIMAL,
    ay                                  DECIMAL,
    az                                  DECIMAL,
    plate_x                             DECIMAL,
    plate_z                             DECIMAL,
    sz_top                              DECIMAL,
    sz_bot                              DECIMAL,
    pfx_x                               DECIMAL,
    pfx_z                               DECIMAL,
    hit_distance_sc                     DECIMAL,
    launch_speed                        DECIMAL,
    launch_angle                        DECIMAL,
    effective_speed                     DECIMAL,
    release_spin_rate                   DECIMAL,
    release_extension                   DECIMAL,
    estimated_ba_using_speedangle       DECIMAL,
    estimated_woba_using_speedangle     DECIMAL,
    launch_speed_angle                  DECIMAL,
    
PRIMARY KEY (game_date, batter, pitcher, events)
);


COMMENT ON TABLE pitch_data IS 'Stores pitch data.';
CREATE INDEX pitch_data_index ON pitch_data (game_date, pitcher);