
CREATE DATABASE skincare_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE skincare_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skin_profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    skin_type ENUM(
        'oily', 'dry', 'normal',
        'combination', 'sensitive', 'unknown'
    ) DEFAULT 'unknown',
    skin_concerns TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE skin_analyses (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    analysis_method ENUM('questionnaire', 'camera') NOT NULL,
    identified_skin_type ENUM(
        'oily', 'dry', 'normal',
        'combination', 'sensitive', 'unknown'
    ) DEFAULT 'unknown',
    questionnaire_answers JSON,
    image_path VARCHAR(255),
    analysis_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- 4. Skincare Products
CREATE TABLE skincare_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT,
    ingredients TEXT,
    suitable_skin_types JSON,
    image_path VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skincare_routines (
    routine_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    analysis_id INT NULL,
    routine_name VARCHAR(150) NOT NULL,
    skin_type VARCHAR(30) NOT NULL,
    routine_period ENUM('morning', 'evening') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (analysis_id)
        REFERENCES skin_analyses(analysis_id)
        ON DELETE SET NULL
);

CREATE TABLE routine_steps (
    step_id INT AUTO_INCREMENT PRIMARY KEY,
    routine_id INT NOT NULL,
    product_id INT NOT NULL,
    step_number INT NOT NULL,
    instructions TEXT,
    UNIQUE (routine_id, step_number),
    FOREIGN KEY (routine_id)
        REFERENCES skincare_routines(routine_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES skincare_products(product_id)
        ON DELETE RESTRICT
);
