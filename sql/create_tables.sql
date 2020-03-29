CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       nickname CHAR(50) NOT NULL,
       email VARCHAR(300),
       mode CHAR(10) NOT NULL DEFAULT 'guest',
       is_deleted BOOLEAN DEFAULT false,
       meta JSON DEFAULT '{}',
       created_on TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
);

CREATE TABLE answers (
       id SERIAL PRIMARY KEY,
       questions VARCHAR(1000) NOT NULL,
       answers VARCHAR(1000) NOT NULL,
       is_deleted BOOLEAN DEFAULT FALSE,
       meta JSON DEFAULT '{}',
       tags TEXT [],
       created_on TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
       updated_on TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
       submitted_by INTEGER REFERENCES users(id) ON DELETE RESTRICT
);
