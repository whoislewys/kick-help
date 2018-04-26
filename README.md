# Kick-Help API
###### Isaiah Discipulo
###### 4.26.2018

### Overview
For this project I created a Python API to predict the success of a Kickstarter campaign. The API uses a neural network to estimate the probability of success for a given campaign. This project was concieved at Sunhacks, in collaboration with Luis Gomez and Sam Rondinelli. I have since spent the last month improving the API as a solo developer.

### Data
###### Training Data
To train the neural network, I used a dataset of Kickstarter projects, posted on Kaggle by user Kemical. The dataset included over 380,000 projects with several parameters, including Kickstarter category, USD goal, duration of fundraising, and project success. Below is a sample of the raw dataset.
```
1000002330,The Songs of Adelaide & Abullah,Poetry,Publishing,GBP,2015-10-09 11:36:00,1000,2015-08-11 12:12:28,0,failed,0,GB,0,,,,
1000004038,Where is Hank?,Narrative Film,Film & Video,USD,2013-02-26 00:20:50,45000,2013-01-12 00:20:50,220,failed,3,US,220,,,,
1000007540,ToshiCapital Rekordz Needs Help to Complete Album,Music,Music,USD,2012-04-16 04:24:11,5000,2012-03-17 03:24:11,1,failed,1,US,1,,,,
1000011046,Community Film Project: The Art of Neighborhood Filmmaking,Film & Video,Film & Video,USD,2015-08-29 01:00:00,19500,2015-07-04 08:35:03,1283,canceled,14,US,1283,,,,
1000014025,Monarch Espresso Bar,Restaurants,Food,USD,2016-04-01 13:38:27,50000,2016-02-26 13:38:27,52375,successful,224,US,52375,,,,
1000023410,Support Solar Roasted Coffee & Green Energy!  SolarCoffee.co,Food,Food,USD,2014-12-21 18:30:44,1000,2014-12-01 18:30:44,1205,successful,16,US,1205,,,,
1000030581,Chaser Strips. Our Strips make Shots their B*tch!,Drinks,Food,USD,2016-03-17 19:05:12,25000,2016-02-01 20:05:12,453,failed,40,US,453,,,,
1000034518,SPIN - Premium Retractable In-Ear Headphones with Mic,Product Design,Design,USD,2014-05-29 18:14:43,125000,2014-04-24 18:14:43,8233,canceled,58,US,8233,,,,
```
Although I do not know how this dataset was generated, I would guess that it was scraped from Kickstarter. 'Scraping' is the act of pulling data from the raw HTML files of a website.
