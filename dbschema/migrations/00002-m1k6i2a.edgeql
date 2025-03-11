CREATE MIGRATION m1k6i2aoufntiyxi7kiqnoivtzwmcdzocc75c6td4vq3rbbifa2g2q
    ONTO m1xpqfd55qva3h6lyfap7cznascb2h45udfn5onblv2tldi53fndaa
{
  ALTER TYPE default::Meeting {
      CREATE PROPERTY end_date: cal::local_date;
      CREATE REQUIRED PROPERTY location: std::str {
          SET default := '';
      };
      CREATE PROPERTY start_date: cal::local_date;
      CREATE REQUIRED PROPERTY title: std::str {
          SET default := '';
      };
  };
};
