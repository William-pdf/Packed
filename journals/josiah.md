## July 11, 2022

Today, I worked on:
* Creating Dockerfile.dev modules for Weather, Currency, and Flights APIs.
* Creating docker-compose.yml incorporating the above as well as React
* Getting the weather api up and running

The group and I discussed whether we wanted to use one microservice per API or whether we should combine them all into one. We went with the former in order to make the webapp as modular as possible. Thankfully, Docker makes this easy!

I recalled from the second module of the bootcamp that our API kees must be kept absolutely secret. I got a chance to dig around stack overflow and Docker docs to figure out how to accomplish this. If you add an .env module to the same directory as the docker-compose module, you can add environment variables which can be declared in the docker-compose using the syntax VARIABLE_NAME: ${VARIABLE_FROM_ENV}


## July 12, 2022

Today, I worked on:
* Updating the return format of the weather api
* Creating two unittests to check the functionality of the weather api

The group and I talked about .env and passing environmental variables via the docker-compose, as mentioned in yesterday's journal.

A learning process for me today was building unittests. Bypassing the actual api call was a bit tricky but with the help of docs I was able to complete it. Using test driven development involves writing more lines of code but I expect it will save incredible amounts of hassle down the road, especially when working with code I did not write.


## July 13, 2022

Today, I worked on:
* Building a fourth FastAPI microservice called locations to be used by the front end form.
* Implementing basic Continuous Integration testing on the weather and locations APIs to run unittests.

The group and I talked about building unit tests for our APIs.

Working with PostgreSQL and Psycopg was a bit of a challenge today. I had an interesting issue where I tried to make a query looking for a specific row from the locations table using a WHERE clause as follows: """...WHERE country LIKE '%%s%';""", (country_variable). I was unable to escape the like clause to inject the value from country_variable. I found another way to make it work and was really happy about it until I realized that the query I was making was not the information I needed in the first place. At least I learned a lot from the docs for PostgreSQL and Psycopg. Next time, I will also plan ahead more.

## July 14, 2022

Today, I worked on:
* Structuring packing list models in exaclidraw
* Updating unit tests for locations and weather
* Creating fake weather api endpoint to save weather tokens while in development
* Researching oauth for react

The group and I discussed modifying the ghi structure so that when a user submits the form, they are presented with the graphs AND can build the packing list on the same page. We also discussed CI/CD variables stored in Gitlab to allow for CI testing.

Today was a tricky because there are two large challenges that lie ahead. Building the Django microservice for packing lists AND implementing oauth. The tricky thing is that I do not know in what sequence to do it. Also, authentication is still a big mystery to me and learning about it is daunting. I looked into a promise based feature for React called Axios that can integrate authentication, but have not learned more yet. After thinking it over, I will likely take the next few days to dive into authentication while the rest of the team work on the front end and Django project.

## July 15, 2022

Today, I worked on:
* Creating a logo for Packed on Canva
* Further authentication research
* Mapping packing list models on excalidraw
* Creating scratchpad directory for packing list suggestion ideas

The group and I discussed the relationships between the models for the packing list project. There was some confusion on the difference between the Condition and Category models but we came to a suitable solution.

Today was a bit of a grind because I am not an expert in logo design. I kept going to websites to find something I like. When I finally found something, they tried to make me pay for it. After a few rounds of that, I finally found something that will work temporarily. On a brighter note, brainstorming a few creative ideas for packing list items was fun! Finally, I learned about token authentication via JWTs stored in localstorage vs cookies. 

## July 18, 2022

Today, I worked on:
* Writing views for packing list
* Pair programming instruction with other teammates
* Configuring settings.py to allow CORS POST requests form selected origins

The group and I spent a lot of time figuring out how to approach the views. We put our primary focus on geting items based on the parameters passed from the frontend. We collectively created the main views to get the app functioning.

Building views is one of my favorite activities so today was a lot of fun. The data we are receiving from the frontend and the data we are returning is formatted in a fairly complex way. I learned that drawing is very useful, especially when trying to explain data structures to others. On another note, I re-learned about where to place any cors management in the list of MIDDLEWARE in settings.py. 

## July 19, 2022

Today, I worked on:
* Writing Category, Item and Condition views
* Creating error handling for views
* Pair programming to troubleshoot Django issues

The group and I spent time coming up with the game plan for the next week. Today, we finished the MVP backend and tomorrow we will work together to fill out the front end. After a couple days of that, we hope to have the frontent at MVP level. We will then look into authentication. We also discussed react component strategies for the packing list creation form.

Today, I learned a bit about making migrations in Django. After altering some fields in the models, it caused a lot of problems and I researched a bit to find a working solution. Also, I came up with a couple ways to make the code for the views more dry via helper functions for error handling. Karmina and I were having trouble getting one of her DELETE views to work and we kept refactoring the code. A SEIR had the idea to restart the docker container and that solved the issue. In the future, that will be one of the things I try if the code looks good.


## July 20, 2022

Today, I worked on:
* Refactoring Django models and views to make names more accurate
* Brainstorming layout of packing list react components
* Working on packing list react components
* Troubleshooting flight API

The group and I spent a significant amount of time discussing how we wanted to layout the packing list page. Eventually, we drew out our plan on excalidraw and divided the tasks. We also worked with William in troubleshooting the flight api. The documentation is quite scarce for that.

I learned a lot about function components and hooks with react. Passing state around a few components is already a pain and I look forward to implementing redux state management in a future project. Unfortunately, I was bug hunting for a good portion of the day. Interestingly, passing state between sibling componenets is a challenge. I ended up createing a useState hook in the siblings' parent component and passed down item and useItem to the child components.

## July 21, 2022

Today, I worked on:
* Further Django view refactoring
* Building packing GHI list components

The group and I spent a lot of time troubleshooting react component issues together. I see an increasing need ot talk through the look of the website as well as nail down the flight API functionality.

Today was another learning experience when it comes to react components. I was having trouble updating the state of the packing list and got help from Zynh, who was able to enlighten me on how to update values correctly when passed down as props. Also, Junella referred me to FontAwesome, a site which allows you to use icons on things like buttons instead of words. It is a very clean look!

## July 22, 2022

Today, I worked on:
* Discussing goals for the next week with the team
* Refactoring packing list front end
* Researching JWT auth (to be integrated next week)

The group and I spent about 45 minutes talking about the game plan for this next week. We are going to switch the priority of the flight aip to be a stretch goal. William is now going to work with Junella on the GHI, Karmina will continue with the packing list suggestions on the front end, and I will integrate authentication. We created issues on gitlab and will abide by the due dates as much as possible.

I talked with several other groups who have integrated auth into their projects and began learning about Simple JWT. We had only about an hour of project time but I will learn more over the weekend.


## July 25, 2022

Today, I worked on:
* Integerating quantities into the packing list
* Preparing to send completed packing list to the backend
* Branstorming GUI look with team

The group and I connected briefly at the start of project time but did not have any updates to go over. Part way through project time, William shared some GUI mockups on slack and the rest of us gave our feedback.

Working with react hooks was a bit slow today. I spent a couple hours trying to touch up the packing list. My big challenge was updating the state with quantities of items. I tried making all sorts of helper functions before finally realizing the solution was right in front of my face. I ended up just copying the state, making a change and then setting the state to the new updated copy (NOTE TO SELF: REMEMBER TO TREAT STATE AS IMMUTABLE)

## July 26, 2022

Today, I worked on:
* Integrating suggested items into packing list
* Building django view to receive packing list
* Deployment research

The group and I connected to discuss some GHI alterations involving weather data and currency. We also discussed the website appearance theme a bit.

I am getting more comfortable with react hooks by the day. What is still very tricky is deployment. I have been preparing this project for deployment a little bit every week but there are a LOT of moving parts to factor in.

## July 27, 2022

Today, I worked on:
* Further refactoring of packing list form
* Building view to handle creation of packing list and items
* Writing instructions for engineers to get the project up and running after a database purge

The group and I briefly discussed the GHI form page. We also discussed handling weather data from the API differently.

Today was slow work with a lot of errors when creating the views to handle the creation of a packing list. I reconfigured the encoders and ended up rebuilding the database a couple of times. In the end, I created a couple helper functions in the views to actually make create the table rows. I also implemented a feature in the views that checks to make sure a user item that was input does not already exist before creating another one. Instructors will be reviewing our project tomorrow so I created a fairly comprehensive step by step to get the project up and running.

## July 28, 2022

Today, I worked on:
* Completed create packing list views
* Integrated Django Rest Framework SimpleJWT auth in the frontend and backend

The group and I discussed goals for the weekend/next week. We also did a bit of pair programming to troubleshoot the refactoring of the weather API.

Today was a large undertaking. I have been putting off implementing authentication but finally jumped in to do it. I learned a lot about custom user models in Django. I also studied up on the React hook, useContext. Keeping track of the JWT's stored in local storage and in the react state was tricky. Writing the functions to refresh tokens periodically was also a huge challenge. However, after today's work, I feel as though I could do this again and take much less time.

## Aug 1, 2022

Today, I worked on:
* Completing sign up functionality
* Building react page to view and edit an already created packing list

The group and I discussed plans for the week. We are looking to complete front end functionality on Wednesday before moving on to aesthetics. Next week, we will work on deployment.

Today was a lot of fun. I am getting much more comfortable with React and building the detail page was a smooth process of switching between the Django views and the React components. Employing the useNavigate hook in conjunction with the useLocation hook was pretty cool to learn about. Also, I was able to reuse one of the other components which made the one I was working on much more DRY. I was worried about implementing the sign up feature, but it turned out to be quite straightforward with Django Rest Framework.

## Aug 2, 2022

Today, I worked on:
* Continuing to build packing list detail page
* User historical item integration
* Continuous Deployment

The group and I talked a lot about the GHI today. Junella found a theme that we are trying to base our look off of. Adding color and various other CSS to the site has breathed life into it. We also talked about the tasks to complete before the end of the week.

Users obviously want to be suggested the items they have packed for trips before. I spent some time updating the views to allow users to be able to do exactly that. I also spent some time learning about css and how to alter the look of the packing list page. After working on that for a while, I dug into continuous deployment. It is a lot of detailed work but will be well worth it when the site is live.

## Aug 3, 2022

Today, I worked on:
* Fixing various errors around the frontend
* Improving the look of the detailed packing list page
* Deploying the site

The group and I spent a good chunk of the morning discussing the GHI and making a game plan to complete it before due date. It was a good chance to give/receive feedback on our work and implement the suggestions.

Today was a struggle for me to implement a feature on the detail packing list page. I still have not gotten it to work and am a bit burned out. I will give it a fresh attempt tomorrow. Deployment has been a good experience overall. I had a bug in the gitlab-ci module that took a while to find but now the website seems to be deployed semi-successfully. Tomorrow, I will go over the steps of deployment with the group.

## Aug 4, 2022

Today, I worked on:
* CSS for DetailList page
* Creating page navigation blocker
* CI/CD
* Linting
* Writing function comments

The group and I collaborated a lot today. Brainstorming and troubleshooting is both fun and very productive. Most of our discussions were about the GHI and completing the project to meet the deadline.

Going into today, I was worried about implementing a page navigation blocker to prevent people from leaving their list with unsaved changes. It turned out to be a very straightforward process. Implementing that is a big user experience improvement. Also, I have really enjoyed deploying the site. As of today, it is fully deployed and operational. The rest of of the work tomorrow will be touching up stuff. Linting my python was easy to do with black and flake8.

## Aug 5, 2022

Today, I worked on:
* Fixing a bug with currency - detaillist integration
* Continuous Integration
* Bug hunting
* Writing the docs

The group and I discussed final goals for the project and how to split up the linting/cleaning/writing docs. I was also able to give a mini lesson on how to deploy the site to the other group member. Hopefully, it will save them trouble down the line.

I thought today was going to be pretty easy in terms of writing the docs. I WAS WRONG. A huge bug involving the currency api and my model structure for packing lists showed up. Thankfully, the rest of the team was able to focus on the docs while I wrote some new endpoints and restructured the DetailList page logic. That aside, the day went very smoothly. I got to learn some new CSS tips and tricks. With the due date coming up in 6 minutes, I am grateful that we completed on time. Myself and the others learned a ton about engineering and teamwork on this project, it was a great experience.
