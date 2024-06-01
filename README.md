# Cloud Computing: exercise 1

A cloud-based (serverless) system to manage a parking lot. 
Price is 10$ per hour (based on 15 minutes increments).
•	Entry: each time a car enters a parking lot, the system records (entry time, license plate and parking lot), and returns a (ticket id).
•	Exit: each time a car exits a parking lot, the system calculates the payment and returns (the charge for the time in the parking lot).

## Getting Started

### Prerequisites

You need to use AWS account and Pulumi account.
- [https://aws.amazon.com]
- [https://www.pulumi.com]

### Installing 

After configuring Pulumi and AWS and installing their CLI, do the following instructions:
- Clone the project locally
- Open commandline to the project's directory
- Run: 
    pulumi up

Pulumi will deploy the system and its requirements. At the end you will receive two URL:
- Entry endpoint: 
  Please pass the plate and parking plot via the link, as follows:
  POST/entry?plate=123-123-123&parkingLot=382
  The systom will show the corresponding ticket id (e.g., 1234).
- Exit endpoint: 
  Please pass the ticket id via the link, as follows:
  POST/exit?ticketId=1234
  The system will show the plate, parking lot, total parked time, and the payment.

In order to delete the system, run:
    pulumi destroy

