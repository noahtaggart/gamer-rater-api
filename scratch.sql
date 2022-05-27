    SELECT
            g.*,
            AVG(r.rating) as "Average Rating"

            from raterapp_game g
            join raterapp_rating r On r.game_id = g.id
            Group By g.id
            ORDER by "average rating" DESC
            Limit 5


    SELECT
            g.*,
            AVG(r.rating) as "Average Rating"
            from raterapp_game g
            join raterapp_rating r On r.game_id = g.id
            Group By g.id
            ORDER by "average rating" asc
            Limit 5

    SELECT
    c.label,
    COUNT(gc.category_id) as "GamesPerCategory"

    from raterapp_game g
    join raterapp_game_category gc on g.id = gc.game_id
    join raterapp_category c on gc.category_id = c.id
    group by g.id
    order by "GamesPerCategory" DESC

    SELECT
    g.*
    from raterapp_game g
    Where g.number_of_players >= 5

    SELECT
    g.*,
    COUNT(r.id) as "Review Count"
    from raterapp_game g
    join raterapp_review r on r.game_id = g.id
    GROUP by g.id
    order by "review count" desc 
    limit 1


                SELECT *
                FROM (
                        SELECT
                            p.*,
                            u.first_name || " " || u.last_name AS full_name,
                            COUNT(g.creator_id) AS games_added
                        FROM raterapp_player p
                        LEFT JOIN raterapp_game g
                            ON p.id = g.creator_id
                        JOIN auth_user u
                            ON p.id = u.id
                        GROUP BY p.id
                )
                WHERE games_added = (
                    SELECT
                        MAX(games_added)
                    FROM (
                        SELECT
                            p.*,
                            COUNT(g.creator_id) AS games_added
                        FROM raterapp_player p
                        LEFT JOIN raterapp_game g
                            ON p.id = g.creator_id
                        GROUP BY p.id
                    )
                )


select 
*
from raterapp_game g 
where g.age_recommendation < 8


SELECT
COUNT(g.id) as NoPhotoCount
from raterapp_game g 
left join raterapp_photo p on p.game_id = g.id
WHERE p.photo ISNULL

SELECT
    p.*,
    u.first_name || " " || u.last_name AS full_name,
    COUNT(r.id) as ReviewCount
    from raterapp_player p
    join raterapp_review r on r.player_id = p.id
    JOIN auth_user u ON p.id = u.id
    GROUP by p.id
    order by ReviewCount desc 
    limit 3

