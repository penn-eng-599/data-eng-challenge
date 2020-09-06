select
    nhl_player_id as id,
    coalesce(max(full_name), 'UNKNOWN') as full_name,
    coalesce(game_team_name, 'UNKNOWN') as team_name,
    sum(coalesce(stats_assists,0)
    + coalesce(stats_power_play_assists,0)
    + coalesce(stats_shorthanded_assists,0)
    + coalesce(goalie_stats_assists, 0)) as assists,
    sum(coalesce(stats_goals,0)
    + coalesce(stats_power_play_goals,0)
    + coalesce(stats_shorthanded_goals,0)
    + coalesce(goalie_stats_goals,0)) as goals,
    sum(coalesce(stats_assists,0)
    + coalesce(stats_power_play_assists,0)
    + coalesce(stats_shorthanded_assists,0)
    + coalesce(goalie_stats_assists, 0)
    + coalesce(stats_goals,0)
    + coalesce(stats_power_play_goals,0)
    + coalesce(stats_shorthanded_goals,0)
    + coalesce(goalie_stats_goals,0)) as points,
    sum(coalesce(
        split_part(stats_time_on_ice::TEXT, ':', 1)::INTEGER * 60
            + split_part(stats_time_on_ice::TEXT, ':', 2)::INTEGER, 0)
    + coalesce(
        split_part(stats_event_time_on_ice::TEXT, ':', 1)::INTEGER * 60
            + split_part(stats_event_time_on_ice::TEXT, ':', 2)::INTEGER, 0)
    + coalesce(
        split_part(stats_power_play_time_on_ice::TEXT, ':', 1)::INTEGER * 60
            + split_part(stats_event_time_on_ice::TEXT, ':', 2)::INTEGER, 0)
    + coalesce(
        split_part(stats_shorthanded_time_on_ice::TEXT, ':', 1)::INTEGER * 60
            + split_part(stats_shorthanded_time_on_ice::TEXT, ':', 2)::INTEGER, 0)
    + coalesce(
        split_part(goalie_stats_time_on_ice::TEXT, ':', 1)::INTEGER * 60
            + split_part(goalie_stats_time_on_ice::TEXT, ':', 2)::INTEGER, 0)) as time_on_ice
from {{ ref('player_game_stats') }}
group by nhl_player_id, game_team_name
