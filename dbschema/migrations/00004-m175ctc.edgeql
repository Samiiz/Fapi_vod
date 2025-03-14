CREATE MIGRATION m175ctc5hvjhdghj5yadqcknxa4bvh7gaeih6otqsbw4teu3ozdqhq
    ONTO m1cuktbmhf5kyok4lzkd3i7ltrc66qygwx5qplgobbwim6ma4wrqba
{
  ALTER TYPE default::Particupant {
      DROP LINK dates;
  };
  ALTER TYPE default::Particupant RENAME TO default::Participant;
  ALTER TYPE default::ParticupantDate RENAME TO default::ParticipantDate;
  ALTER TYPE default::Participant {
      CREATE MULTI LINK dates := (.<participant[IS default::ParticipantDate]);
  };
};
