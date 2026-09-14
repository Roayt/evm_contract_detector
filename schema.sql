CREATE TABLE contract(
    id               bigint  GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,
    address          varchar(42), 
    chain            text,          --Evm Chain
    symbol           text,          --Evm Chain symbol
    blocknumber      bigint,           --Evm Chain blocknumber
    created_at       timestamptz DEFAULT now(), --block produced time

    UNIQUE (address,chain)

)

