CREATE MIGRATION m17sska6ytwat33iyigjmzj6z6ue2vdoqx4omgsu4vsrl2akasrm3a
    ONTO m1uwekrn4ni4qs7ul7hfar4xemm5kkxlpswolcoyqj3xdhweomwjrq
{
  ALTER TYPE default::Movie {
      CREATE INDEX ON (.title);
  };
};
