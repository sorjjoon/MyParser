SELECT (
        (SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)
        /
        (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))
         + 
         (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))
         /
         (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) 
         
         ) AS "avg";

 SELECT count(*) FROM Match WHERE LOG_ID IN(1,2) as x
 
     
SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))+ (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) ) AS "avg";



      