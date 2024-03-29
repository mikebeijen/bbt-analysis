# BBTFind Analysis Scripts

## File: ```args.py```

#### Inputs
- JSON export of the `bbtArguments` collection from MongoDB.
#### Outputs
- CSV file with time constraint from the experimental condition.
- CSV file with every line being an argument to rate in terms of task performance metrics

## File: ```ratedArgs.py```
#### Inputs
- Second output of ```args.py```, but with arguments rated
#### Outputs
- CSV file with following data: average T-Depth, D-Qual, D-Intrp, number of argument submitted

## File: ```logs.py```
Should be run for every set of logs.
#### Inputs
- JSON export of the LogUI logs.
#### Outputs
- CSV file with following data: number of queries issued per minute, average length of queries issued in words, average length of queries issued in characters, number of results clicked, deepest rank of search results visited, average rank of search results visited, number of SERPs visited, dwell time on SERPs per minute (H), time used in total.

## File: ```pretask.py```
#### Inputs
- JSON export of the `bbtPretask` collection from MongoDB.
#### Outputs
- CSV file with following data: gender, age, education, wse, prior knowledge, prior interest,task definition

## File: ```posttask.py```
#### Inputs
- JSON export of the `bbtPosttask` collection from MongoDB.
#### Outputs
- CSV file with following data: ATI, user experience, perception of time pressure

## File: ```condition.py```
#### Inputs
- JSON export of the `bbtCondition` collection from MongoDB. 
#### Outputs
- CSV file with prolific ID and experimental condition

## File: ```listReliance.py```
#### Inputs
- JSON export of the LogUI logs.
- JSON export of the `bbtArguments` collection from MongoDB.
#### Outputs
- CSV file with the prolific ID and the the highest cosine similarity between a webpage and the submitted arguments.