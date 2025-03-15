with
    name := <str>$name,
    url_code := <str>$url_code,
    dates := <array<cal::local_date>>$dates,
    PARTICIPANT := (
        insert Participant {
            name := name,
            meeting := (
                select Meeting
                filter .url_code = url_code
            )
        }
    ),
    DATES := (
        for date in array_unpack(dates)
        insert ParticipantDate {
          participant := PARTICIPANT,
          date := date,
        }
    ),
select DATES {id, participant};
