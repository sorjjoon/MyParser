SELECT (
        (SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)
        /
        (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))
         + 
         (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))
         /
         (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) 
         
         ) AS "avg";

 
     
SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))+ (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) ) AS "avg";




SELECT COUNT(case match_player.side when 1 then 1 else null end) as player_side, COUNT(case match_player.side when 0 then 1 else null end) as player_against, player.name FROM match_player
JOIN player ON player.id= match_player.player_id
WHERE match_player.match_id IN (126, 125) GROUP BY player_id ORDER BY (player_side+player_against) DESC;
