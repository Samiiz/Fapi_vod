with
    url_code := <str>$url_code,
select Meeting {url_code, start_date, end_date, location, title}
filter .url_code = url_code
limit 1
