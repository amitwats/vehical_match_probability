## Vehicle Matching Code Challenge

You have been provided with a SQL script that creates two tables: `vehicle` and `listing` (`data.sql`). 
To start working on this code challenge, you will need to set up a local Postgresql database and run the script to insert the necessary tables and data.

**Vehicle Table**

The `vehicle` table is a structured catalogue of vehicle variants, segmented by Make, Model, Badge, Fuel Type, Transmission Type and Drive Type.

**Listing Table**

The `listing` table contains records of vehicle listings that have been posted to online marketplaces (Gumtree, Facebook Marketplace, etc).

Each `listing` record is linked back to the corresponding `vehicle` record that describes the type of car being sold.

**Description Input File**

You've also been provided with a file that contains car descriptions (`inputs.txt`). 

In this file, each line corresponds to a different car description. 
The descriptions are in plain text, and resemble the type of car descriptions that you might find on a car listing marketplace.

The car descriptions might be very detailed and specify every attribute of the car, but they could also be vague and/or inaccurate.
For example, some descriptions might not specify the fuel type of the car (Diesel, Petrol or Hybrid-Petrol).

## Requirements

You must create a Python or Node.js program that finds a matching Vehicle ID for each description in the provided `input.txt` file.

The output of your program must show the matching Vehicle ID for each description, as well as a confidence score from 0 to 10. 
A confidence score of 0 would indicate a very uncertain match, whereas a confidence score of 10 would indicate that the match was definitely correct.

For example, if the description did not specify the transmission type of the car, the confidence score would likely be lower than a description that did specify the transmission type (Automatic or Manual).

If there are multiple vehicles which you find to be the most likely match, you should return the vehicle which has the most listings associated with it in the `listing` table.

Your program must interact with the `vehicle` and `listing` tables by running SQL queries from within your program. You should not need to edit the SQL data.

You can use a combination of regular expressions, sql and standard algorithms/logic to match the vehicles. Your program should print the vehicle match response for each of the provided test cases - both the matching vehicle ID as well as the confidence score.

## Example Output

Your program output should contain a result for **all** of the descriptions in the input file, but below you can find an example for a select few descriptions.

```
Input: Volkswagen Golf 110TSI Comfortline Petrol Automatic Front Wheel Drive
Vehicle ID: 4749339721203712
Confidence: 9

Input: VW Amarok Ultimate 
Vehicle ID: 4951649860714496
Confidence: 7

Input: VW Golf R with engine swap from Toyota 86 GT
Vehicle ID: 5824662093168640
Confidence: 6
```