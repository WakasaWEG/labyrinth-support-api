USE labyrinth_support_db;

INSERT INTO roles (name)
VALUES
    ('player'),
    ('admin')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO users (email, password_hash, nickname, is_banned)
VALUES
    ('alice@example.com', '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvabcd', 'Alice', 0),
    ('bob@example.com', '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvabcd', 'Bob', 0),
    ('admin@example.com', '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvabcd', 'Admin', 0),
    ('banned@example.com', '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvabcd', 'BannedUser', 1)
ON DUPLICATE KEY UPDATE
    nickname = VALUES(nickname),
    is_banned = VALUES(is_banned);

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON
    (u.email = 'alice@example.com' AND r.name = 'player') OR
    (u.email = 'bob@example.com' AND r.name = 'player') OR
    (u.email = 'admin@example.com' AND r.name = 'player') OR
    (u.email = 'admin@example.com' AND r.name = 'admin') OR
    (u.email = 'banned@example.com' AND r.name = 'player')
ON DUPLICATE KEY UPDATE assigned_at = assigned_at;

INSERT INTO player_progress (user_id, level, xp, soft_currency, hard_currency)
SELECT id, 1, 0, 100, 0
FROM users
ON DUPLICATE KEY UPDATE
    level = VALUES(level),
    xp = VALUES(xp),
    soft_currency = VALUES(soft_currency),
    hard_currency = VALUES(hard_currency);

INSERT INTO leaderboard_scores (user_id, score)
SELECT id, 0
FROM users
ON DUPLICATE KEY UPDATE score = leaderboard_scores.score;

INSERT INTO inventory (user_id, item_code, quantity)
SELECT id, 'torch', 1
FROM users
WHERE email IN ('alice@example.com', 'bob@example.com')
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

INSERT INTO inventory (user_id, item_code, quantity)
SELECT id, 'healing_herb', 3
FROM users
WHERE email = 'alice@example.com'
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

INSERT INTO inventory (user_id, item_code, quantity)
SELECT id, 'rusty_sword', 1
FROM users
WHERE email = 'bob@example.com'
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

INSERT INTO runs (id, user_id, status, started_at, ended_at)
SELECT
    1,
    u.id,
    'extracted',
    NOW(3) - INTERVAL 2 DAY,
    NOW(3) - INTERVAL 2 DAY + INTERVAL 18 MINUTE
FROM users u
WHERE u.email = 'alice@example.com'
ON DUPLICATE KEY UPDATE
    status = VALUES(status),
    started_at = VALUES(started_at),
    ended_at = VALUES(ended_at);

INSERT INTO runs (id, user_id, status, started_at, ended_at)
SELECT
    2,
    u.id,
    'dead',
    NOW(3) - INTERVAL 1 DAY,
    NOW(3) - INTERVAL 1 DAY + INTERVAL 11 MINUTE
FROM users u
WHERE u.email = 'bob@example.com'
ON DUPLICATE KEY UPDATE
    status = VALUES(status),
    started_at = VALUES(started_at),
    ended_at = VALUES(ended_at);

INSERT INTO runs (id, user_id, status, started_at, ended_at)
SELECT
    3,
    u.id,
    'started',
    NOW(3) - INTERVAL 5 MINUTE,
    NULL
FROM users u
WHERE u.email = 'alice@example.com'
ON DUPLICATE KEY UPDATE
    status = VALUES(status),
    started_at = VALUES(started_at),
    ended_at = VALUES(ended_at);

INSERT INTO run_results (run_id, is_success, rooms_visited, loot_value, duration_seconds, ended_reason)
VALUES
    (1, 1, 6, 250, 1080, 'exit'),
    (2, 0, 4, 90, 660, 'death')
ON DUPLICATE KEY UPDATE
    is_success = VALUES(is_success),
    rooms_visited = VALUES(rooms_visited),
    loot_value = VALUES(loot_value),
    duration_seconds = VALUES(duration_seconds),
    ended_reason = VALUES(ended_reason);

UPDATE leaderboard_scores ls
JOIN users u ON u.id = ls.user_id
SET ls.score = CASE
    WHEN u.email = 'alice@example.com' THEN 250
    WHEN u.email = 'bob@example.com' THEN 0
    WHEN u.email = 'admin@example.com' THEN 0
    WHEN u.email = 'banned@example.com' THEN 0
    ELSE ls.score
END;

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    1,
    'run_start',
    JSON_OBJECT('note', 'Seed extracted run')
FROM users u
WHERE u.email = 'alice@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    1,
    'room_enter',
    JSON_OBJECT('roomNumber', 1, 'roomType', 'start_room')
FROM users u
WHERE u.email = 'alice@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    1,
    'loot_found',
    JSON_OBJECT('itemCode', 'gold_coin', 'quantity', 25)
FROM users u
WHERE u.email = 'alice@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    1,
    'run_finish',
    JSON_OBJECT('isSuccess', true, 'endedReason', 'exit', 'lootValue', 250)
FROM users u
WHERE u.email = 'alice@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    2,
    'run_start',
    JSON_OBJECT('note', 'Seed failed run')
FROM users u
WHERE u.email = 'bob@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    2,
    'enemy_killed',
    JSON_OBJECT('enemyType', 'slime', 'count', 2)
FROM users u
WHERE u.email = 'bob@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    2,
    'player_death',
    JSON_OBJECT('reason', 'trap_damage')
FROM users u
WHERE u.email = 'bob@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    2,
    'run_finish',
    JSON_OBJECT('isSuccess', false, 'endedReason', 'death', 'lootValue', 90)
FROM users u
WHERE u.email = 'bob@example.com';

INSERT INTO game_events (user_id, run_id, event_type, payload_json)
SELECT
    u.id,
    3,
    'run_start',
    JSON_OBJECT('note', 'Active run for API tests')
FROM users u
WHERE u.email = 'alice@example.com';