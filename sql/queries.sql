-- 1. список всех студентов
SELECT id, name, group_name
FROM students
ORDER BY id;

-- 2. список всех мероприятий с сортировкой по названию
SELECT id, name, max_duration
FROM events
ORDER BY name;

-- 3. фильтрация (where 1): выступления с длительностью не более 8 минут
SELECT id, title, duration
FROM presentations
WHERE duration <= 8;

-- 4. фильтрация (where 2): студенты определенной группы
SELECT id, name, group_name
FROM students
WHERE group_name = 'ЭФБО-16-24';

-- 5. соединение таблиц (join 1): полная информация о выступлениях
SELECT
    p.id,
    p.title,
    p.duration,
    p.score_1,
    p.score_2,
    s.name AS student_name,
    s.group_name,
    e.name AS event_name,
    e.max_duration
FROM presentations p
JOIN students s ON p.student_id = s.id
JOIN events e ON p.event_id = e.id;

-- 6. соединение таблиц (join 2): детальная информация по конкретному выступлению
SELECT
    p.id,
    p.title,
    p.duration,
    p.score_1,
    p.score_2,
    s.name AS student_name,
    s.group_name,
    e.name AS event_name,
    e.max_duration
FROM presentations p
JOIN students s ON p.student_id = s.id
JOIN events e ON p.event_id = e.id
WHERE p.id = 1;

-- 7. агрегатные функции (1): общее число выступлений и средний балл
SELECT
    COUNT(id) AS total_presentations,
    AVG(score_1) AS avg_score_1,
    AVG(score_2) AS avg_score_2
FROM presentations;

-- 8. агрегатные функции (2): минимальная и максимальная длительность доклада
SELECT
    MIN(duration) AS min_duration,
    MAX(duration) AS max_duration
FROM presentations;

-- 9. группировка (group by 1): подсчет количества выступлений в каждом мероприятии
SELECT
    e.id,
    e.name,
    COUNT(p.id) AS presentations_count
FROM events e
LEFT JOIN presentations p ON e.id = p.event_id
GROUP BY e.id, e.name;

-- 10. группировка с фильтрацией (group by 2 + having): мероприятия со средним баллом от 4.5
SELECT
    e.name,
    AVG(p.score_1 + p.score_2) AS avg_total_score
FROM events e
JOIN presentations p ON e.id = p.event_id
GROUP BY e.id, e.name
HAVING AVG(p.score_1 + p.score_2) >= 4.5;

-- 11. подзапрос (not in): поиск мероприятий без выступлений
SELECT id, name
FROM events
WHERE id NOT IN (
    SELECT DISTINCT event_id FROM presentations
);

-- 12. обновление записи
UPDATE events
SET max_duration = 15
WHERE id = 1;

-- 13. удаление записи
DELETE FROM presentations
WHERE id = 999;
