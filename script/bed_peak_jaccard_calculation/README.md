# A script for BEDTools Jaccard score calculation
This hadoop streaming mapper script can read a input line containing ids of two ChIP-Seq experiemnts and fetch the corresponding peak call bed files from a MySQL database. Then it uses BEDTools Jaccard utility to calculate the Jaccard score and peak intersection between those two files. Result score is saved in another MySQL table.

## Usage
  <pre><code>
  python bed_peak_mapper.py [-h] [-H MYSQL_HOST] [-P MYSQL_PORT] -n MYSQL_DBNAME
                          -u MYSQL_USER -p MYSQL_PASS -f FILE_PATH
  </code></pre>

## Options
  <pre><code>
  -h, --help                        Show this help message and exit
  -H / --mysql_host MYSQL_HOST      MySQL server host name, default: localhost
  -P / --mysql_port MYSQL_PORT      MySQL server port id, default: 3306
  -n / --mysql_dbname MYSQL_DBNAME  MySQL server database name
  -u / --mysql_user MYSQL_USER      MySQL server user name
  -p / --mysql_pass MYSQL_PASS      MySQL server password name
  -f / --file_path FILE_PATH        File path prefix
  </code></pre>
  
## Requirement
  * pymysql
  * pybedtools
  * BEDTools2  
