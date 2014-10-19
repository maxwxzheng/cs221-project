select 
	distinct(title.id) as movie_id,
    title.title as title,
    movie_info_idx.info as rating,
    t3.info as votes,
    t4.info as gross,
    t2.info as countries
from title JOIN 
	(movie_info_idx, 
	 movie_info AS t2, 
	 movie_info_idx AS t3,
	 movie_info AS t4) 
ON 
	(movie_info_idx.movie_id = title.id AND t2.movie_id = title.id AND t3.movie_id = title.id and t4.movie_id = title.id) 
WHERE 
	movie_info_idx.info_type_id= 101 AND
	t2.info_type_id = 8 and t2.info = 'USA' AND 
	t3.info_type_id = 100 AND t3.info > 1000 AND
	t4.info_type_id = 107 and t4.info like "%$%(USA)";
	