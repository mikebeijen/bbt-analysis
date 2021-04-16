# BBTFind Analysis Scripts

## File: ```args.py```

#### Inputs
- JSON export of the `bbtArguments` collection from MongoDB.
#### Outputs
- CSV file with time used to complete the submission and argument count per submission.
- CSV file with every line being an argument to rate in terms of task performance metrics

## File: ```ratedArgs.py```
#### Inputs
- Second output of ```args.py```, but with arguments rated
#### Outputs
- CSV file with following data: average T-Depth, D-Qual, D-Intrp

## File: ```logs.py```
Should be run for every set of logs.
#### Inputs
- JSON export of the LogUI logs.
- First output of ```args.py```.
#### Outputs
- CSV file with following data: number of queries issued per minute, average length of queries issued in words, average length of queries issued in characters, number of results clicked, deepest rank of search results visited, average rank of search results visited, number of SERPs visited, dwell time on SERPs per minute (H)

## File: ```pretask.py```
#### Inputs
- JSON export of the `bbtPretask` collection from MongoDB.
#### Outputs
- CSV file with following data: gender, age, education, wse, prior knowledge, prior interest,task definition
