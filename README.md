### Prerequisites
* The Cloud Cost Optimizer requires Python3- Python 3.4 or newer installed.

### Installation
```
$ python3 -m pip install requests
$ pip3 install urllib3
$ pip3 install grequests
$ pip3 install numpy
$ pip3 install boto3
```

### Usage
```
$ python3 CCO.py
```
this command executes the Optimizer

As an input, the optimizer receives the specification of the desired workload. It includes the resource requirements for each of the components comprising the workload, the connections between the components, and additional constraints. analyzes this specification and calculates the mapping of the workload components to cloud resources (VM instances) that minimizes the expected monetary cost of deploying the application over a public cloud.


## Parameters
The file **input_fleet.json** is an example of an input (input_fleet_instructions.json has further information).
The user's workload should be in the **input_fleet.json** 
#### Example of an input json file:
```
{
    "selectedOs": "linux",
    "spot/onDemand": "spot",
    "region": ["eu-south-1", "eu-west-3", "us-east-2","us-east-1"],
    "filterInstances": ["a1","t3a","c5a.xlarge"],
    "Architecture": "all",
    "apps": [
        {
            "app": "App1",
            "share": true,
            "components": [
                {
                    "memory": 8,
                    "vCPUs": 4,
                    "network": 5,
                    "behavior": "terminate",
                    "frequency": "2",
                    "storageType": null,
                    "affinity": "Comp2",
                    "name": "Comp1",
                },
                {
                    "memory": 8,
                    "vCPUs": 3,
                    "network": 0,
                    "behavior": "hibernate",
                    "frequency": "3",
                    "storageType": null,
                    "burstable": true,
                    "anti-affinity": "Comp3",
                    "name": "comp2"
                },
                                {
                    "memory": 8,
                    "vCPUs": 3,
                    "network": 0,
                    "behavior": "hibernate",
                    "frequency": "3",
                    "storageType": null,
                    "burstable": true,
                    "name": "comp5"
                }
            ]
        },
        {
            "app": "App2",
            "share": false,
            "components": [
                {
                    "memory": 10,
                    "vCPUs": 5,
                    "network": 0,
                    "behavior": "stop",
                    "frequency": "4",
                    "storageType": null,
                    "burstable": true,
                    "name": "Comp3"
                }
            ]
        }
    ]
}
```

Where we can see an input of two Applications (App1, App2), which uses linux as their Operation System.
App1 includes three components (Comp1, Comp2, Comp5), and App2 includes only one component (Comp3). each component
has different resource requirements, which described by their memory, vCPUs

### Required parameters:
* selectedOs - operating system (OS) for the workloads
* spot/onDemand - choose instances pricing option- **spot / on-Demand**


### Configuration file:
Configuration file (config) encustomization of default configurations based on individual preferences.
#### Example of a Configuration file:
```
{
    "Data Extraction (always / onceAday / Never)": "onceAday",
    "boto3 (enable / disable)": "disable",
    "Provider (AWS / Azure / Hybrid)": "AWS",
    "Brute Force": "False",
    "Time per region": 1,
    "Candidate list size": 100,
    "Proportion amount node/sons": 0.0005,
    "Verbose": "True"
}
```
* Data Extraction- The frequency with which the data will be extracted
* boto3- Do the information retrieval using boto3. Note that in the case of enable, the data extraction process will be slower
* Provider- which cloud provider should be supported
* Brute Force- boolean parameter, indicates if the CCO should use BF In order to find the optimal solution, or not. Note that this algorithm suitable for less than 7 components. Otherwise, use Local Search Algorithm (explained below)
* [Other Parameters are hyperparameters](#hyperParameter) for the [Local Search algorithm](#local-search-algorithm-description)


## Results
The output of the Optimizer is a fleet_results.json file containing  a list of configurations. Each configuration represents an assignment of all application components to AWS instances.

### Example of the Result
```
[
    {
        "price": 0.275,
        "instances": [
            {
                "onDemandPrice": 0.204,
                "region": "us-east-2",
                "cpu": "8",
                "ebsOnly": true,
                "family": "General purpose",
                "memory": "16",
                "network": "Up to 10 Gigabit",
                "os": "Linux",
                "typeMajor": "a1",
                "typeMinor": "2xlarge",
                "storage": "EBS only",
                "typeName": "a1.2xlarge",
                "discount": 81,
                "interruption_frequency": "<20%",
                "interruption_frequency_filter": 4.0,
                "spot_price": 0.0394,
                "Price_per_CPU": 0.004925,
                "Price_per_memory": 0.0024625,
                "components": [
                    {
                        "appName": "App2",
                        "componentName": "Comp3"
                    }
                ]
            },
            {
                "onDemandPrice": 0.344,
                "region": "us-east-2",
                "cpu": "8",
                "ebsOnly": false,
                "family": "Compute optimized",
                "memory": "16",
                "network": "Up to 10 Gigabit",
                "os": "Linux",
                "typeMajor": "c5ad",
                "typeMinor": "2xlarge",
                "storage": "1 x 300 NVMe SSD",
                "typeName": "c5ad.2xlarge",
                "discount": 78,
                "interruption_frequency": "<5%",
                "interruption_frequency_filter": 0.0,
                "spot_price": 0.076,
                "Price_per_CPU": 0.0095,
                "Price_per_memory": 0.00475,
                "components": [
                    {
                        "appName": "App3",
                        "componentName": "Comp4"
                    }
                ]
            },
            {
                "onDemandPrice": 0.6912,
                "region": "us-east-2",
                "cpu": "16",
                "ebsOnly": true,
                "family": "Compute optimized",
                "memory": "32",
                "network": "25 Gigabit",
                "os": "Linux",
                "typeMajor": "c6gn",
                "typeMinor": "4xlarge",
                "storage": "EBS only",
                "typeName": "c6gn.4xlarge",
                "discount": 77,
                "interruption_frequency": "5%-10%",
                "interruption_frequency_filter": 1.0,
                "spot_price": 0.1596,
                "Price_per_CPU": 0.009975,
                "Price_per_memory": 0.0049875,
                "components": [
                    {
                        "appName": "App1",
                        "componentName": "Comp1"
                    },
                    {
                        "appName": "App1",
                        "componentName": "comp2"
                    },
                    {
                        "appName": "App1",
                        "componentName": "comp5"
                    }
                ]
            }
        ],
        "region": "us-east-2"
    },
    {
        "price": 0.3,
        ...
    }
]
```

## Local Search Algorithm Description

The algorithm Is split into epochs.
each epoch is a combination of 2 phases:
  - **searching** - search for combiniation with minimal price. the search is based on Simulated Annealing and Stochastic Hill Climbing.
  - **selecting the next node to start searching from** -
    -  selects randomly.

#### Search Algorithm
the search is based on Simulated Annealing and Stochastic Hill Climbing.


