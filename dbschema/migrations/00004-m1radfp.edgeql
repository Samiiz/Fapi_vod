CREATE MIGRATION m1radfpuucibl4i4h75y3dliykmvfqc2mawa2hdgiyrdxgd3dvtndq
    ONTO m1n5yjleno2et4us6c566q7awclhhqe3emgu55ogt6zykdsw3rl4pq
{
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE REQUIRED PROPERTY created_at: cal::local_datetime {
          SET default := (cal::to_local_datetime(std::datetime_current(), 'Asia/Seoul'));
          SET readonly := true;
      };
  };
  CREATE TYPE default::Meeting EXTENDING default::Auditable {
      CREATE REQUIRED PROPERTY url_code: std::str {
          SET readonly := true;
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
