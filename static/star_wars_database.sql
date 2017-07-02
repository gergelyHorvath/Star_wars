DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


DROP TABLE IF EXISTS votes;
DROP SEQUENCE IF EXISTS votes_id_seq;
CREATE TABLE votes (
    id serial NOT NULL,
    planet_id integer NOT NULL,
    planet_name character varying(255) NOT NULL,
    nick_name character varying(255),
    phone_number character varying(100) NOT NULL,
    user_id integer NOT NULL,
    submission_time char(16) default to_char(LOCALTIMESTAMP, 'YYYY-MM-DD HH24:MI')
);


INSERT INTO users VALUES (1, 'Greg', 'sha256$tYOWxXmp$9943b1c652ee8478af53cba3b6865e0b8b6553cca569c7517293b605ff0585ba');
INSERT INTO users VALUES (2, 'kepi', 'sha256$yc5uGltT$6195f8d3c4557658b6fc7b6e77be8d500fb2f8c71f82d7456a8ac431241ead18');


SELECT pg_catalog.setval('users_id_seq', 2, true);


ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT username_uk UNIQUE (username);

ALTER TABLE ONLY votes
    ADD CONSTRAINT votes_pk PRIMARY KEY (id);

ALTER TABLE ONLY votes
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
