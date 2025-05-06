use spotify_db;

### Q1 find out the highest popularity each album
SELECT  album , MAX(popularity) as max_popularity 
from spotify_tracks 
GROUP BY album
ORDER BY max_popularity DESC;

## Q2 find out second highest popularity 
SELECT  max(popularity) as second_highest_popularity
from spotify_tracks
WHERE popularity not in (SELECT max(popularity) from spotify_tracks);

## Q3 find out average values of popularity
SELECT avg(popularity) 
from spotify_tracks ;

## Q4 determine distinct values of spotify_tracks table 
SELECT DISTINCT track_name , album 
from spotify_tracks ;

## ## Q5 determine the count of table 
SELECT count(*)
from spotify_tracks ;

## aggregate functions like sum 
SELECT sum(popularity) as total_popularity
from spotify_tracks;

## case functions 

SELECT 
	case
		WHEN popularity >=80 THEN "high popularity"
        	WHEN popularity >=50 THEN "popularity"
		ELSE "less popularity"
    	END as popularity_tracks ,
    count(*) as count_of_tracks 
from spotify_tracks 
GROUP BY 1;


Q6 order by based on popularity and limit functions
select * 
from 
order by popularity desc
limit = 1
