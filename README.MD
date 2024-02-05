# Flight deal search project
*This project is based on Angela Yu's course on Python (Day 39). The code was written entirely by me - I only used the initial instructions*

You can find the course here: https://www.udemy.com/course/100-days-of-code/

## APIs used
To complete this project, it was recommended to use those APIs:
- https://sheety.co/ - accessing my Google Sheets,
- https://partners.kiwi.com/ - searching flights, airports and prices,
- https://www.twilio.com/docs/sms - sending myself an SMS on price change.

All those platforms allow accessing the data for free (Twilio gives 15$ free credit for trial).

## How this works

This project works on my personal Google Sheet. It can be adjusted for any other Google Sheet by changing the endpoint for Sheety. Its main goal is to practice: 
- OOP, 
- API calls, 
- working with JSON, 
- understanding documentation.

In short: when program runs, it checks if new locations were added to the spreadsheet. If so, it updates it with IATA airport codes.
Next step is comparing the prices. "FLY_FROM" (check - Kiwi documentation) parameter is based on my local airport - "POZ", but it can be changed to any other airport on the go. It takes all codes from the spreadsheet and checks the lowest price for the flight in next 6 months. As a last step - if there is a lower price than the current one in the spreadsheet, it first updates it and then sends an SMS to my phone number with an information how it changed.