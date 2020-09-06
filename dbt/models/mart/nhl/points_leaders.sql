select
    team_name,
    full_name,
    points
from {{ ref('nhl_players') }} t
where 3 > (
    select count(tt.full_name)
    from {{ ref('nhl_players') }} tt
    where t.points < tt.points
        and t.team_name = tt.team_name
        and points != 0
)
and points != 0
order by team_name, points desc, full_name
