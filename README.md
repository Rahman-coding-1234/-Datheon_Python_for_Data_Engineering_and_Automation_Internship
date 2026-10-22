\# Datheon Python for Data Engineering \& Automation Internship



A small Python ETL pipeline built as part of the Datheon internship program.



\## What it does



1\. \*\*Extract:\*\* reads raw customer data from `data/customers\_raw.csv`.

2\. \*\*Transform:\*\* removes rows without a name, trims spaces, and keeps only the latest record per customer.

3\. \*\*Load:\*\* writes clean data into a SQLite database (`data/app.db`) using upserts (insert or update on conflict), inside a transaction.

4\. \*\*Verify:\*\* runs quality checks (row count, duplicate IDs, null names).

5\. \*\*Schedule:\*\* runs the full pipeline every day at 09:00 using the `schedule` library, and logs each run to `logs/pipeline.log`.



