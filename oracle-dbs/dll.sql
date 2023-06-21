-- TABLES

CREATE TABLE fundapec_pymts (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(255),
    doc_num VARCHAR2(255),
    career VARCHAR2(3),
    terms VARCHAR2(6),
    credits NUMBER,
    amount NUMBER,
    ref_num VARCHAR2(10),
    insert_date DATE
);