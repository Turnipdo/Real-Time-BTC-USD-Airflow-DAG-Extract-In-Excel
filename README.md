# Real-Time-BTC-USD-Airflow-DAG-Extract-In-Excel :atom:
Using yfinance, we grab minute-by-minute BTC-USD data, dump it into PostgreSQL, and link Excel via ODBC for quick analysis!

## Requirements :basecamp:
* `Airflow`
* `Docker Desktop`
* `VSCode`
* `Excel`
* `DBeaver`
* `ODBC Driver PostgreSQL`

## Additional info :warning:
* To be able to connect to a PostgreSQL database, this [video](https://www.youtube.com/watch?v=S1eapG6gjLU&t=502s) explains a step by step process on how to establish a connection on the Web UI and using `DBeaver`.
* I strongly recommend that you learn how to build/extend the Airflow Docker image to download the right modules and dependencies (if you don't know how to do so). Here's a link to a YouTube video I followed, which worked really well: [Link to the video](https://www.youtube.com/watch?v=0UepvC9X4HY&t=376s).
* I've attached the Dockerfile with the bash scripts, along with the requirements.txt, to install the correct dependencies and modules. You can then build/extend your Docker image.
* In your `Docker-Compose.yaml` file, I personally used the default PostgreSQL config provided. If you don't have this in the 'services' section of the YAML file, please include it.

## Instructions :page_with_curl:
If you have Airflow set up with the correct image extension and all its dependencies, I will show you how to set up the PostgreSQL ODBC driver on your Windows computer.

* First, verify the host machine firewall settings if they're allowing connections: :earth_americas::bricks: <br>
  * Go to `Control-Panel`.
  * Click on `System and Security`.
  * Find and Click `Windows Defender Firewall`.
  * Click on `Allow an app or feature through Windows Defender Firewall`.
  * Look for `Docker Desktop Backend` and ensure there are two rows each ticked for the Private and Public networks.

* Second, create an inbound rule: :earth_americas::shield: <br>
  * Go to `Control-Panel`.
  * Click on `System and Security`.
  * Find and Click `Windows Defender Firewall`.
  * Click on `Advanced Settings` :arrow_right: `Inbound Rule` :arrow_right: `New Rule`
  * Choose `Port` and click `Next`
  * Select `TCP` and specify port `5432`
  * Allow the connection and click `Next`
  * Select when this rule applies (I selected all three `Domain`, `Private`, `Public`)
  * Name the rule whatever you want hit finish.
  

* Third, once you've downloaded the [ODBC Driver for postgreSQL](https://www.postgresql.org/ftp/odbc/releases/REL-16_00_0005/), you need to configure it: :car: <br>
  * On Windows, type "ODBC" in the `Start Menu`.
  * Select whichever bit version your Excel runs on (`32 bit` or `64 bit`).
  * Navigate to :arrow_right: `User DSN`.
  * Click on `Add`.
  * Select the `PostgreSQL Unicode` driver.
  * Click on `Finish`.

* Third, you want to configure it: :memo: <br>
  * Name it however you want in the `data source` section.
  * You can input an optional `description` if you'd like.
  * Enter the `database name` you are connecting to in your airflow connection (in my case it's called 'test)'.
  * Enter the `server name`, if it's on your local machine it's just `localhost`.
  * Enter 5432 for your `Port`.
  * Enter the username and password for the postgreSQL login (this is shown in the `Docker-compose.yaml` file under the postgreSQL services).
  * Click the drop-down menu on `SSL Mode` and select 'prefer'.
  * CLick on `Test` to ensure the connection works.


I'll explain some important parts of the code that I think need attention.
* For the python DAG script:
  * Notice in the DAG, in order to establish a succesful connection to the database, you must use a `PostgresHook(postgres_conn_id='name_of_connection_defined_in_WebUI')`.
  * You have to then use the `.get_conn()` method followed by the `.cursor()` method in order to do any kind of data modificaitons.
  * It is imperative to then use the `.executemany(sql_script, dataframe.values.tolist())` method to execute your query.
  * If you want to see those changes being made, then you will see the I had to use the `.commit()` method.
  * You have to close the connection and the cursor with the `.close()` method once you're done. However, if you have another task that needs to run more SQL queries, you   shouldn't close the connection yet.
  * In the SQL code, notice the section 'ON CONFLICT (timestamp) DO NOTHING.' This ensures that existing timestamps in the table will not be overridden, and only new timestamp values will be added.
 
* For the Power Query M script:
  * It's similar to my previous mini project where I extracted values from Excel workbooks in order to feed it into a SQL code.
  * Except we're not reading the values from the workbook, we're simply going to fill those values in.
  * This is the format you want it in: Odbc.Query("Driver={PostgreSQL Unicode};Server=localhost;Database=test;","SELECT * FROM table_name")
  * You can find more info about this function by navigating to this [Link](https://learn.microsoft.com/en-us/powerquery-m/odbc-query).
 
## Before and after photos of your Excel table after hitting refresh every couple of minutes :camera_flash:

### Before (# of rows = 191)

![Before](https://github.com/Turnipdo/Real-Time-BTC-USD-Airflow-DAG-Extract-In-Excel/blob/main/images/Before.png?raw=true)

### After (# of rows = 196)

![After](https://github.com/Turnipdo/Real-Time-BTC-USD-Airflow-DAG-Extract-In-Excel/blob/main/images/After.png?raw=true)




