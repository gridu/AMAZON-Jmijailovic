-- Performs function on the aggregate rows over a 10 second tumbling window for a specified column.
CREATE OR REPLACE STREAM "INTERMEDIATE_STREAM" (
   "category"   VARCHAR(16),
   "numOfViews" integer);
-- Create a pump which continuously selects from a source stream (SOURCE_SQL_STREAM_001)
-- joins against a table named CompanyName on the ticker_symbol column
-- and inserts into output stream (DESTINATION_SQL_STREAM)
CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "INTERMEDIATE_STREAM"
SELECT STREAM *
        FROM TABLE (TOP_K_ITEMS_TUMBLING(CURSOR(SELECT STREAM * FROM "SOURCE_SQL_STREAM_001" JOIN VIEWS as v
  ON "SOURCE_SQL_STREAM_001"."item_id" = v."item_id"),'category',10,300));


CREATE OR REPLACE STREAM "TRIGGER_STREAM" ("category" VARCHAR(16), "numOfViews" integer);
CREATE OR REPLACE PUMP "CATEGORIES_WITH_100_VIEWS" AS INSERT INTO "TRIGGER_STREAM"
SELECT STREAM "category", "numOfViews"
    FROM (SELECT "category", "numOfViews" FROM "INTERMEDIATE_STREAM") WHERE "numOfViews">100;