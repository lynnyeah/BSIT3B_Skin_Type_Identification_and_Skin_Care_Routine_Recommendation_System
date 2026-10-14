
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skin_types (
    skin_type_id INT AUTO_INCREMENT PRIMARY KEY,
    skin_type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE assessment_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL
);

CREATE TABLE skin_assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skin_type_id INT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (skin_type_id) REFERENCES skin_types(skin_type_id)
);

CREATE TABLE skincare_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(50),
    description TEXT
);


CREATE TABLE skincare_recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    skin_type_id INT NOT NULL,
    product_id INT,
    routine_time ENUM('Morning', 'Evening', 'Both') NOT NULL,
    instructions TEXT,
    FOREIGN KEY (skin_type_id) REFERENCES skin_types(skin_type_id),
    FOREIGN KEY (product_id) REFERENCES skincare_products(product_id)
);

