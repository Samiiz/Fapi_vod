CREATE MIGRATION m1cuktbmhf5kyok4lzkd3i7ltrc66qygwx5qplgobbwim6ma4wrqba
    ONTO m1k6i2aoufntiyxi7kiqnoivtzwmcdzocc75c6td4vq3rbbifa2g2q
{
  CREATE TYPE default::Particupant EXTENDING default::Auditable {
      CREATE REQUIRED LINK meeting: default::Meeting;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  ALTER TYPE default::Meeting {
      CREATE MULTI LINK participants := (.<meeting[IS default::Particupant]);
  };
  CREATE TYPE default::ParticupantDate EXTENDING default::Auditable {
      CREATE REQUIRED LINK participant: default::Particupant {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED PROPERTY date: cal::local_date;
      CREATE CONSTRAINT std::exclusive ON ((.date, .participant));
      CREATE REQUIRED PROPERTY enabled: std::bool {
          SET default := true;
      };
      CREATE REQUIRED PROPERTY stared: std::bool {
          SET default := false;
      };
  };
  ALTER TYPE default::Particupant {
      CREATE MULTI LINK dates := (.<participant[IS default::ParticupantDate]);
  };
};
