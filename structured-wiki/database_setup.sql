CREATE TABLE IF NOT EXISTS views (
    name text UNIQUE
);

CREATE UNIQUE INDEX IF NOT EXISTS views_name_index ON views(name);

CREATE TABLE IF NOT EXISTS objects (
    object_id int not null, 
    version int int not null,
    view int REFERENCES views,
    data json,
    primary key(object_id, version)
);

CREATE INDEX IF NOT EXISTS version_index ON objects(version);