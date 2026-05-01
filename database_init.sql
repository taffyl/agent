CREATE DATABASE IF NOT EXISTS "trade_db";

CREATE TABLE IF NOT EXISTS "trades" (

    "id" SERIAL PRIMARY KEY,

    "item_id" INTEGER NOT NULL,
    "item_name" VARCHAR(255) NOT NULL,
    "item_number" INTEGER NOT NULL,
    
    "buyer_id" INTEGER NOT NULL,
    "buyer_name" VARCHAR(255) NOT NULL,

    "seller_id" INTEGER NOT NULL,
    "seller_name" VARCHAR(255) NOT NULL,

    "trade_comment" VARCHAR(255) NOT NULL,
    "total_price" FLOAT NOT NULL,
    "trade_start_time" TIMESTAMP NOT NULL,
    "trade_state" VARCHAR(255) NOT NULL
    "trade_delivery_warehouse" VARCHAR(255) NOT NULL,
    "trade_delivery_time" TIMESTAMP

);


CREATE TABLE IF NOT EXISTS "items" (

    "id" SERIAL PRIMARY KEY,

    "item_name" VARCHAR(255) NOT NULL,
    "item_inventory" INTEGER NOT NULL,
    "item_price" FLOAT NOT NULL,
    "item_description" VARCHAR(255) NOT NULL,
    "item_category" VARCHAR(255) NOT NULL,
)

CREATE TABLE IF NOT EXISTS "buyers"(

    "id" SERIAL PRIMARY KEY,

    "buyer_name" VARCHAR(255) NOT NULL,
    "buyer_phone" VARCHAR(255) NOT NULL,
    "buyer_email" VARCHAR(255) NOT NULL,
    "buyer_address" VARCHAR(255) NOT NULL,
    "buyer_credit_card" VARCHAR(255) NOT NULL,
    "buyer_credit_card_expiration" VARCHAR(255) NOT NULL,

)


