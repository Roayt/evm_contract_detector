CREATE TABLE contract(
    id               bigint  GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,
    deployer_address         varchar(42),
    contract_address          varchar(42), 
    chain            text,          --Evm Chain
    symbol           text,          --Evm Chain symbol
    blocknumber      bigint,           --Evm Chain blocknumber
    created_at       timestamptz DEFAULT now(), --time at which row was inserted

    CONSTRAINT contract_address_chain_key UNIQUE (contract_address,chain)

)

