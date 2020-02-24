explain query plan
SELECT COUNT(case match_player.side when 1 then 1 else null end) as player_side, 
        COUNT(case match_player.side when 0 then 1 else null end) as player_against,
        SUM(case match_player.side when 1 then COALESCE(match.round3,match.round2 ,0) else null end) / cast(COUNT(case match_player.side when 1 then 1.0 else null end)as float) as player_with_win_pre,
        SUM(case match_player.side when 0 then COALESCE(match.round3,match.round2 ,0) else null end) / cast(COUNT(case match_player.side when 0 then 1.0 else null end)as float) as player_against_win_pre,
        player.name as name,
        player.player_class as class 
        FROM "match_player"
        JOIN player ON player.id= match_player.player_id
        JOIN match ON match.id = match_player.match_id
        WHERE match.id IN  (1,2,3,4,5) 
        GROUP BY player.name 
        ORDER BY COUNT(case match_player.side when 1 then 1 else null end) + COUNT(case match_player.side when 0 then 1 else null end) DESC;        
  
