
--stats queries (the IN clauses have example data in them)


SELECT (
       ((SELECT COALESCE(avg(round2),0)*count(round2)
       from match
       WHERE LOG_ID IN(1,2) AND round3 is null)
       +
       (SELECT COALESCE(avg(round3),0)*count(round3)
       from match
       WHERE LOG_ID IN(1,2)))
       /
       (SELECT count(*)
       FROM Match
       WHERE LOG_ID IN(1,2)) 
       ) AS "avg";


--(same but postgre syntax)
SELECT (((SELECT COALESCE(avg(round2::int),0)*count(round2)
       from match
       WHERE LOG_ID IN (1,2,3) AND round3 is null)+(SELECT COALESCE(avg(round3::int),0)*count(round3::int)
       from match
       WHERE LOG_ID IN (1,2,3)))/(SELECT count(*)
       FROM Match
       WHERE LOG_ID IN (1,2,3)) ) AS avg
--Times user has played with other players: 

SELECT COUNT(case match_player.side when true then 1 else null end) as player_side,
       COUNT(case match_player.side when false then 1 else null end) as player_against,
       player.name
FROM "match_player"
       JOIN player ON player.id= match_player.player_id
WHERE match_player.match_id IN (1, 2,3,4,5,6,7,8)
GROUP BY player.name
ORDER BY COUNT(case match_player.side when true then 1 else null end) + COUNT(case match_player.side when false then 1 else null end) DESC;
--note, order by clause is the same as ORDER BY(player_side+player_against), but this syntax won't work in postgre


--Win rate when playing with a certain a player (note in the app for perfomance this queue is bundled with the one above)
SELECT COUNT(case match_player.side when true then 1 else null end) as player_side,
       COUNT(case match_player.side when false then 1 else null end) as player_against,
       SUM(case match_player.side when true then COALESCE(match.round3::int,match.round2 :: int,0) else null end) / cast(COUNT(case match_player.side when true then 1.0 else null end)as decimal) as player_with_win_pre,
       SUM(case match_player.side when false then COALESCE(match.round3::int,match.round2 :: int,0) else null end) / cast(COUNT(case match_player.side when false then 1.0 else null end)as decimal) as player_against_win_pre,
       player.name
FROM "match_player"
       JOIN player ON player.id= match_player.player_id
       JOIN match ON match.id = match_player.match_id
       JOIN log ON log.id = match.log_id
WHERE match.id IN (1, 2)
GROUP BY player.name
ORDER BY COUNT(case match_player.side when true then 1 else null end) + COUNT(case match_player.side when false then 1 else null end) DESC;

