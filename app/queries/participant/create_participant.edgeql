with
    name := <str>$name,
    url_code := <str>$url_code,
insert Participant {
    name := name,
    meeting := (
        select Meeting
        filter .url_code = url_code
    )
}
