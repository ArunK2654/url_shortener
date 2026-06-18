Commands

pip install psycopg2, redis
uvicorn app.main:app --reload

Postgres:
docker run --name postgre-sql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=urlshortener -p 5432:5432 -d postgres
docker exec -it postgre-sql psql -U postgres -d urlshortener
\dt
\d 
select * from urls;
\q

redis caching:
docker run --name redis-cache -p 6379:6379 -d redis
docker exec -it redis-cache redis-cli
KEYS * - To show all the keys
GET d - To get value of the key
SET test hello - To set key and value
SET product1 mobile EX 60
TTL product1 - To see the expiry time for a key
DEL product1
EXISTS product1
DBSIZE - To count keys
FLUSHDB - To delete all the cache
MONITOR - cache logs dont use in production
INFO stats - keyspace_hits, keyspace_misses

redis rate limiter:
INCR product1 -- gives 1 used as counter(key is product1 and value is 1)
EXPIRE product1 60 -- expiry in 60 secs
INCR product1 -- gives value 2
INCR product1 -- gives value 3
INCR product1 -- gives value 4


docker compose up --build