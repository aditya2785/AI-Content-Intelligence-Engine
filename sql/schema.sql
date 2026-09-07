DROP TABLE IF EXISTS interactions;
DROP TABLE IF EXISTS content;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    user_id VARCHAR(20) PRIMARY KEY,
    country VARCHAR(100),
    age_group VARCHAR(20),
    signup_date TIMESTAMP,
    following_count INTEGER,
    creator_flag BOOLEAN,
    preferred_genres TEXT
);


CREATE TABLE creators (
    creator_id VARCHAR(20) PRIMARY KEY,
    creator_name VARCHAR(150),
    signup_date TIMESTAMP,
    creator_type VARCHAR(100),
    followers INTEGER
);


CREATE TABLE content (
    content_id VARCHAR(20) PRIMARY KEY,
    creator_id VARCHAR(20),
    content_type VARCHAR(50),
    genre VARCHAR(100),
    created_at TIMESTAMP,
    duration DOUBLE PRECISION,
    tags TEXT,
    is_template BOOLEAN,
    is_recreation BOOLEAN,

    CONSTRAINT fk_content_creator
        FOREIGN KEY (creator_id)
        REFERENCES creators(creator_id)
);


CREATE TABLE interactions (
    interaction_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(20),
    content_id VARCHAR(20),
    creator_id VARCHAR(20),
    genre VARCHAR(100),
    content_type VARCHAR(50),
    duration DOUBLE PRECISION,
    creator_followers INTEGER,
    content_created_at TIMESTAMP,
    timestamp TIMESTAMP,
    clicked INTEGER,
    liked INTEGER,
    saved INTEGER,
    shared INTEGER,
    commented INTEGER,
    recreated INTEGER,
    meaningful_engagement INTEGER,
    watch_time DOUBLE PRECISION,
    completion_rate DOUBLE PRECISION,
    impression INTEGER,

    CONSTRAINT fk_interaction_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_interaction_content
        FOREIGN KEY (content_id)
        REFERENCES content(content_id),

    CONSTRAINT fk_interaction_creator
        FOREIGN KEY (creator_id)
        REFERENCES creators(creator_id)
);
