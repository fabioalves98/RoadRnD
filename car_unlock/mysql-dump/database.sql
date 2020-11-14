USE unlockDB;
DROP TABLE IF EXISTS nfc;
CREATE TABLE nfc(id VARCHAR(10) PRIMARY KEY, tag VARCHAR(255) UNIQUE);
INSERT INTO nfc(id, tag) VALUES('AA-01-AA', "tag1");
INSERT INTO nfc(id, tag) VALUES('GD-02-XA', "tag2");
INSERT INTO nfc(id, tag) VALUES('LD-34-CV', "tag3");
INSERT INTO nfc(id, tag) VALUES('RT-10-SA', "tag4");
