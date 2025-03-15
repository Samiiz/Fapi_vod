with
    url_code := <str>$url_code,
select Meeting {
    url_code,
    start_date,
    end_date,
    title,
    location,
    participants: {
        id,
        name,
        dates: {
            id,
            date,
            starred,
            enabled
        } order by .date
    }
}
filter .url_code = url_code
limit 1
