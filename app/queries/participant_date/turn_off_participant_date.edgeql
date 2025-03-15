with
    participant_date_id := <uuid>$participant_date_id,
update ParticipantDate
filter .id = participant_date_id
set {enabled := false, starred := false};