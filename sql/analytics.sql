
SELECT
    COUNT(*) AS total_interactions,
    SUM(clicked) AS total_clicks,
    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(watch_time)::NUMERIC,
        2
    ) AS avg_watch_time,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate,

    SUM(meaningful_engagement) AS meaningful_engagements,

    ROUND(
        (100.0 * SUM(meaningful_engagement) / COUNT(*))::NUMERIC,
        2
    ) AS meaningful_engagement_rate
FROM interactions;

-- 2. Daily Active Users

SELECT
    DATE(timestamp) AS activity_date,
    COUNT(DISTINCT user_id) AS dau
FROM interactions
GROUP BY DATE(timestamp)
ORDER BY activity_date;

-- 3. Daily engagement metrics

SELECT
    DATE(timestamp) AS activity_date,

    COUNT(*) AS interactions,

    COUNT(DISTINCT user_id) AS active_users,

    SUM(clicked) AS clicks,

    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate

FROM interactions

GROUP BY DATE(timestamp)

ORDER BY activity_date;

-- 4. Top-performing content
-- Compare both engagement volume and engagement efficiency.

SELECT
    content_id,

    COUNT(*) AS impressions,

    SUM(clicked) AS clicks,

    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    SUM(meaningful_engagement) AS meaningful_engagements,

    ROUND(
        (
            100.0 * SUM(meaningful_engagement)
            / COUNT(*)
        )::NUMERIC,
        2
    ) AS engagement_rate_percent,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate

FROM interactions

GROUP BY content_id

HAVING COUNT(*) >= 20

ORDER BY engagement_rate_percent DESC

LIMIT 20;

-- 5. Creator performance
-- Compare creator size, exposure, and engagement efficiency.

SELECT
    c.creator_id,
    c.creator_name,
    c.followers,

    COUNT(i.interaction_id) AS impressions,

    SUM(i.clicked) AS clicks,

    ROUND(
        (
            100.0 * SUM(i.clicked)
            / NULLIF(COUNT(i.interaction_id), 0)
        )::NUMERIC,
        2
    ) AS ctr_percent,

    SUM(i.meaningful_engagement)
        AS meaningful_engagements,

    ROUND(
        (
            100.0 * SUM(i.meaningful_engagement)
            / NULLIF(COUNT(i.interaction_id), 0)
        )::NUMERIC,
        2
    ) AS engagement_rate_percent,

    ROUND(
        AVG(i.completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate

FROM creators c

LEFT JOIN interactions i
    ON c.creator_id = i.creator_id

GROUP BY
    c.creator_id,
    c.creator_name,
    c.followers

HAVING COUNT(i.interaction_id) >= 20

ORDER BY engagement_rate_percent DESC

LIMIT 20;

-- 6. Genre performance

SELECT
    genre,

    COUNT(*) AS impressions,

    SUM(clicked) AS clicks,

    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate,

    SUM(meaningful_engagement)
        AS meaningful_engagements

FROM interactions

GROUP BY genre

ORDER BY meaningful_engagements DESC;

-- 7. Content type performance

SELECT
    content_type,

    COUNT(*) AS impressions,

    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(watch_time)::NUMERIC,
        2
    ) AS avg_watch_time,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate,

    SUM(meaningful_engagement)
        AS meaningful_engagements

FROM interactions

GROUP BY content_type

ORDER BY meaningful_engagements DESC;


-- 8. Engagement by age group

SELECT
    u.age_group,

    COUNT(i.interaction_id) AS interactions,

    COUNT(DISTINCT u.user_id) AS active_users,

    ROUND(
        (
            100.0 * SUM(i.clicked)
            / COUNT(i.interaction_id)
        )::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(i.completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate,

    SUM(i.meaningful_engagement)
        AS meaningful_engagements

FROM users u

JOIN interactions i
    ON u.user_id = i.user_id

GROUP BY u.age_group

ORDER BY ctr_percent DESC;


-- 9. Engagement by hour of day

SELECT
    EXTRACT(HOUR FROM timestamp) AS hour_of_day,

    COUNT(*) AS interactions,

    COUNT(DISTINCT user_id) AS active_users,

    ROUND(
        (100.0 * SUM(clicked) / COUNT(*))::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate

FROM interactions

GROUP BY EXTRACT(HOUR FROM timestamp)

ORDER BY hour_of_day;

-- 10. New vs Returning Users

WITH first_activity AS (
    SELECT
        user_id,
        MIN(DATE(timestamp)) AS first_activity_date
    FROM interactions
    GROUP BY user_id
)

SELECT
    DATE(i.timestamp) AS activity_date,

    COUNT(DISTINCT i.user_id) AS active_users,

    COUNT(
        DISTINCT CASE
            WHEN DATE(i.timestamp) = f.first_activity_date
            THEN i.user_id
        END
    ) AS new_users,

    COUNT(
        DISTINCT CASE
            WHEN DATE(i.timestamp) > f.first_activity_date
            THEN i.user_id
        END
    ) AS returning_users

FROM interactions i

JOIN first_activity f
    ON i.user_id = f.user_id

GROUP BY DATE(i.timestamp)

ORDER BY activity_date;

-- 10. Content performance by freshness

SELECT
    CASE
        WHEN content_age_days < 1 THEN '0-1 days'
        WHEN content_age_days < 7 THEN '1-7 days'
        WHEN content_age_days < 30 THEN '7-30 days'
        WHEN content_age_days < 90 THEN '30-90 days'
        ELSE '90+ days'
    END AS content_age_bucket,

    COUNT(*) AS impressions,

    COUNT(DISTINCT content_id) AS unique_content,

    SUM(clicked) AS clicks,

    ROUND(
        (
            100.0 * SUM(clicked)
            / COUNT(*)
        )::NUMERIC,
        2
    ) AS ctr_percent,

    ROUND(
        AVG(completion_rate)::NUMERIC,
        3
    ) AS avg_completion_rate,

    SUM(meaningful_engagement)
        AS meaningful_engagements,

    ROUND(
        (
            100.0 * SUM(meaningful_engagement)
            / COUNT(*)
        )::NUMERIC,
        2
    ) AS meaningful_engagement_rate

FROM interactions

GROUP BY
    CASE
        WHEN content_age_days < 1 THEN '0-1 days'
        WHEN content_age_days < 7 THEN '1-7 days'
        WHEN content_age_days < 30 THEN '7-30 days'
        WHEN content_age_days < 90 THEN '30-90 days'
        ELSE '90+ days'
    END

ORDER BY
    MIN(content_age_days);