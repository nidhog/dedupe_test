dedupe_test
===========

Testing <a href="https://github.com/datamade/dedupe"> dedupe</a>

Input Data
----------
Input data is automatically generated using the locu api, in case there is no internet connection you can use your own data.
To use your own data, insert a 'data.csv' file in this form:

| Id  |   name   |
| --- | -------- |
|  1  | Octopops |
|  2  | Despicable Octopus Restaurant |

Output Data
-----------
The output data is in this format:

| Cluster ID | Id |   name   |
| ---------- |--- | -------- |
|      1     | 1  | Octopops |
|      2     | 2  | Despicable Octopus Restaurant |
