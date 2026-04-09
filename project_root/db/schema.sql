CREATE DATABASE IF NOT EXISTS labyrinth_support_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE labyrinth_support_db;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(64) NOT NULL,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    last_login_at DATETIME(3) NULL,
    is_banned TINYINT(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
    INDEX idx_user_roles_role_id (role_id)
) ENGINE=InnoDB;

CREATE TABLE player_progress (
    user_id INT PRIMARY KEY,
    level INT NOT NULL DEFAULT 1,
    xp INT NOT NULL DEFAULT 0,
    soft_currency INT NOT NULL DEFAULT 0,
    hard_currency INT NOT NULL DEFAULT 0,
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_progress_level CHECK (level >= 1),
    CONSTRAINT chk_progress_xp CHECK (xp >= 0),
    CONSTRAINT chk_progress_soft CHECK (soft_currency >= 0),
    CONSTRAINT chk_progress_hard CHECK (hard_currency >= 0)
) ENGINE=InnoDB;

CREATE TABLE inventory (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_code VARCHAR(64) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_inventory_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_inventory_quantity CHECK (quantity >= 0),
    UNIQUE KEY uq_inventory_user_item (user_id, item_code),
    INDEX idx_inventory_user (user_id)
) ENGINE=InnoDB;

CREATE TABLE runs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('started', 'extracted', 'dead') NOT NULL DEFAULT 'started',
    started_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ended_at DATETIME(3) NULL,
    CONSTRAINT fk_runs_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_runs_user_started (user_id, started_at),
    INDEX idx_runs_status (status)
) ENGINE=InnoDB;

CREATE TABLE run_results (
    run_id BIGINT PRIMARY KEY,
    is_success TINYINT(1) NOT NULL,
    rooms_visited INT NOT NULL DEFAULT 0,
    loot_value INT NOT NULL DEFAULT 0,
    duration_seconds INT NOT NULL DEFAULT 0,
    ended_reason ENUM('exit', 'death') NOT NULL,
    CONSTRAINT fk_run_results_run
        FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE,
    CONSTRAINT chk_run_results_rooms CHECK (rooms_visited >= 0),
    CONSTRAINT chk_run_results_loot CHECK (loot_value >= 0),
    CONSTRAINT chk_run_results_duration CHECK (duration_seconds >= 0)
) ENGINE=InnoDB;

CREATE TABLE leaderboard_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_leaderboard_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_leaderboard_user (user_id),
    INDEX idx_leaderboard_score (score),
    CONSTRAINT chk_leaderboard_score CHECK (score >= 0)
) ENGINE=InnoDB;

CREATE TABLE game_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    run_id BIGINT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload_json JSON NOT NULL,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_game_events_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_game_events_run
        FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE SET NULL,
    INDEX idx_game_events_user_time (user_id, created_at),
    INDEX idx_game_events_run_time (run_id, created_at),
    INDEX idx_game_events_type_time (event_type, created_at)
) ENGINE=InnoDB;