CREATE MIGRATION m1g73yw2zfblebqkuxvydm4kqjvcvazbfshnz4cgrpaqlxpfia7ftq
    ONTO m175ctc5hvjhdghj5yadqcknxa4bvh7gaeih6otqsbw4teu3ozdqhq
{
  ALTER TYPE default::ParticipantDate {
      ALTER PROPERTY stared {
          RENAME TO starred;
      };
  };
};
