-- Objective: Membuat ddl untuk Dataset Postgres di  Docker


BEGIN;

-- Create table
CREATE TABLE dataset (
    "Territory" VARCHAR(256),
    "Year" VARCHAR(256),
    "Power_Requirement_Net_Crore_Units" VARCHAR(256),
    "Availability_Of_Power_Net_Crore_Units" VARCHAR(256),
    "Availability_Of_Power_Per_Capita_kiloWatt-Hour" VARCHAR(256),
    "Installed_Power_Capacity_MegaWatt" VARCHAR(256)
);

COMMIT;

BEGIN;

-- Import the csv file into the table
COPY dataset 
FROM '/files/dataset.csv' -- Sesuaikan path ini sesuai dengan lokasi file CSV dalam container PostgreSQL docker
DELIMITER ','
CSV HEADER;

COMMIT;
