INSERT INTO app_user (id, name, email, shift_start, shift_end, user_type) VALUES
(1, 'Bob', 'bob@gmail.com', '2024-02-21 09:03:43', '2024-02-21 10:00:00', 0),
(2, 'Sam', 'sam@gmail.com', '2024-02-21 09:56:55', '2024-02-21 10:00:00', 1),
(3, 'Tyler', 'tyler@gmail.com', '2024-02-21 09:30:26', '2024-02-21 10:00:00', 2),
(4, 'Will', 'will@gmail.com', '2024-02-21 09:45:32', '2024-02-21 10:00:00', 1),
(5, 'Dyllan', 'dyllan@gmail.com', '2024-02-21 10:05:38', '2024-02-21 10:30:00', 1)
ON CONFLICT(id)
DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    shift_start = EXCLUDED.shift_start,
    shift_end = EXCLUDED.shift_end,
    user_type = EXCLUDED.user_type
;