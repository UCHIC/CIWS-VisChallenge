# 2020 Cyberinfrastructure for Intelligent Water Supply (CIWS) Data Visualization Challenge

This folder contains the results for the 2020 visualization challenge. Winning submissions are located in the [submissions](https://github.com/UCHIC/CIWS-VisChallenge/tree/master/2020_Challenge/submissions) folder. All of the following information was used to introduce the challenge and provide information and materials to participants. It is recorded here for archival purposes. 

## Information Meeting Materials

[View the Information Meeting flyer.](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/2020_Challenge/doc/2020_Visualization_Challenge_Info_Meeting_Flyer.pdf)

We held an initial information meeting on Wednesday October 21, 2020 at 5:00 PM at which participants had the opportunity to meet the challenge sponsors, get ideas, and ask questions. See the following links for the information meeting materials, including a recording of the meeting.

* [PowerPoint slides presented at the meeting](https://usu.box.com/s/npedrgkl6mx1u0f4ayffzvun3xvnno4t)
* [Zoom recording for the meeting](https://usu.box.com/s/0nzelptxdhksgpwiyuyf3peeod6v8htx)
* [Code examples presented by Camilo and Nour](https://github.com/UCHIC/CIWS-VisChallenge/tree/master/2020_Challenge/examples)

## The Challenge

[View the challenge flyer.](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/2020_Challenge/doc/2020_Visualization_Challenge_Flyer.pdf)

Our research group is developing cyberinfrastructure to better support the collection, management, and use of smart water metering data. This Challenge provides students at Utah State University with an opportunity to develop potentially novel and innovative visualizations of high resolution residential water use data. For this year's challenge, we aim to develop new approaches for providing visual feedback directly to residential water users about their own water use.

Given high temporal resolution water use data from the water meter for a residential home (see the section below about the dataset), we want you to develop visualizations that would be useful in communicating the timing, volume, and distribution of water use within the home. What useful information could be extracted from the data and presented to the homeowner that might influence their water use behavior?

Visualizations devloped for this challenge should be focused on creating visual information that would be useful for residential water users to inform them about thier own water consumption. Given this, the objective is to create visualizations that are easily understandable and may provide actionable information (e.g., the homeowner can see thier water use visually and may change their behavoir based on the information you provide).

[Access Information About our Research Group's Project Here](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/doc/project_summary.md)

**NOTE: We held an initial challenge during 2018-2019. You can find results of the challenge, including the winning entries [here](https://github.com/UCHIC/CIWS-VisChallenge/tree/master/2018-2019_Challenge).

## Prizes!!

We are offering prizes for the most innovative submissions:

* **First Place**: $1000 
* **Second Place**: $750 
* **Third Place**: $500

**Note:** Payment will be made to you by Utah State University through USU's Scholarship Office.

## Who Can Participate?

We are happy to receive submissions from any students at USU. Participants may be at the undergraduate or graduate level.

## Getting Started and How to Submit an Entry

Use the following steps to download the datasets and get started:

1. Click the link in the datasets section below. This will take you to a description of the challenge dataset with links for downloading the files. 
2. Create a new GitHub repository under your GitHub user account to develop and host the source code and/or other files for your submission.
3. Check the [documentation page](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/doc/relevant_literature.md) where we have provided links to documents and papers providing examples of analyses and visualizations relevent to this type of data. You may get some good ideas from these existing papers, but don't let them constrain your creativity!
4. Develop your submission. We encourage you to use Python and existing Python visualization packages such as matplotlib, but you may develop your submission in your preferred programming language or using the tools of your choice. 
5. When complete, commit your source code to your repository and send a link to your repository to jeff.horsburgh@usu.edu.
6. Attend the final Challenge Event (likely virtual - details will be posted on this repository) at the end of the challenge to present your results and do demos for a panel of students and faculty who will select Challenge winners.

**IMPORTANT NOTE:** Our project is focused on open source code development. A condition of receiving prizes for winning entries as part of this challenge will be that you must allow us to upload your source code and/or submission files to this GitHub repository. 

## See How Submissions Will be Scored

We have developed and posted a rubric for scoring the submissions to the challenge. You can access the rubric [here](https://github.com/UCHIC/CIWS-VisChallenge/tree/master/2020_Challenge/doc/Evaluation_Rubric.pdf) so you make sure that your submission checks all of the boxes.

## The Datasets

We've posted a dataset for the challenge that consists of high resolution water use data for an individual household. It consists of the the following files:

* The raw water use data measured on the residential water meter for the house at approximately 4 second resolution (one observation every 4 seconds).
* Disaggregated and classified water use events (i.e., showers, toilet flushes, faucet events, etc.) for that household derived from the raw water use data. These events were not measured, but were derived from the raw data using a disaggregation/classification algorithm.

[Access the Challenge Datasets Here](https://github.com/UCHIC/CIWS-VisChallenge/tree/master/2020_Challenge/data/readme.md)

## Visit the Documentation Pages

We have developed a set of documentation pages that provide background about our research project along with links to supporting literature. You may find ideas for developing innovative and effective visualizations of the datasets at the link below.

[Access Additional Documentation](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/doc)

## Important Dates

The Challenge is ongoing! The following are important dates:

* **Submission Deadline**: Friday December 4, 2020 by 11:59 PM (see above for how to submit). 
* **Judging Event**: We are targeting December 10th for the final event. Details about time and place (likely virtual) will be provided to all participants who submit an entry to the challenge.

## Contacts

* For information about the Visualization Challenge, the challenge dataset, or if you have general questions, contact Jeff Horsburgh at jeff.horsburgh@usu.edu

## Sponsors and Credits
[![NSF-1552444](https://img.shields.io/badge/NSF-1552444-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1552444)

The material in this repository is based on work supported by National Science Foundation Grant CBET [1552444](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1552444). Any opinions, findings, and conclusions or recommendations expressed are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

