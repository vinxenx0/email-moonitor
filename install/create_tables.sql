CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    token VARCHAR(255) UNIQUE,
    active BOOLEAN DEFAULT FALSE,
    registered_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    config JSON,
    role VARCHAR(20) NOT NULL DEFAULT 'usuario'
);


CREATE TABLE Log (
    id INT PRIMARY KEY,
    user_id INT,
    page VARCHAR(255) NOT NULL,
    event VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    /* FOREIGN KEY (user_id) REFERENCES user(id) */
);
