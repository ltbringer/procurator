# Procurator

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cde256097f2348f39f9a2488bb2ab3dd)](https://www.codacy.com/manual/AmreshVenugopal/procurator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ltbringer/procurator&amp;utm_campaign=Badge_Grade)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
![Last commit](https://img.shields.io/github/last-commit/ltbringer/procurator)

Helps people talk to you in your absence.

At times you are the only person who knows answer to certain specific things. Maybe because of your profession or
it is a problem you faced, and now each time it rears its head again you would be needed. If you consider these situations
as distractions to something more important at hand, this project is supposed to help. Personally speaking, sometimes
I forget replying to people because by the time I am free they are asleep or unavailable (majorly close family members). 
At work there are questions that float around like: 

1. What's the wifi password?
2. How do I use the printer/scanner?
3. Where do you keep _that_ thing?
4. _this_ thing stopped working how do we make it work again?
5. What are the numbers of that _project_?

This project lets you create snapshots of such information. It also allows someone to access it naturally (more work needed here).
Clearing the distraction. Kind of like having a proxy for yourself doing all the boring things for you. More details on how it works [later](#working). 

Some of these questions are a good fit for this project. Answers that don't change frequently, are easy to maintain.
Like the first 2 questions are not going to change on a daily/weekly/monthly basis.

## Name
procurator /ˈprɒkjʊreɪtə/

noun: procurator; plural noun: procurators

Law: an agent representing others in a court of law in countries retaining Roman civil law.
        (in Scotland) a lawyer practising before the lower courts.

![word-usage](https://www.gstatic.com/onebox/dictionary/etymology/en/desktop/adc8de134fe7081488d1ecb22f470da58eba3003a0838886073e0882f54caf09.png)

## Project
This project was created as a part of a 1-day voice-themed Hackathon at [vernacular.ai](https://github.com/Vernacular-ai). 
Support for different platforms, installation, optimization took a backseat for the sake of prototype. 
Read about [future plans](#future-works).

### Current Support
- Ubuntu 18.04
- Python: 3.6.5

### Installation
1. Clone this project.
 
2. Run `poetry install` to install all dependencies.

3. Pull postgres' docker image
    ```bash
    docker pull postgres
    ```
4. Start the postgres container.
 
5. Enter the container using `docker exec -it <container-id> bash`
 
6. In the psql cli Run the following:
    ```sql
    CREATE DATABASE procurator;
    CREATE USER <user> WITH PASSWORD '<safepassword>';
    ALTER ROLE <user> SET client_encoding to 'utf-8';
    ALTER ROLE <user> SET timezone to 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE procurator TO <user>;
    ```

7. Pull kaldi-serve's docker image. - Optional
    ```bash
    docker pull vernacularai/kaldi-serve:master
    ```   
8. Start the kaldi-serve container. - Optional
 
9. To setup the database with the right roles, and seed data, run:
    ```
    poetry run proxy-init --host=<host> --port=<port> --user=<user> --password=<password> --dbname=procurator
    
    # port should be same as the args supplied to the docker container.
    # user, password should be <user>, <password> from step 6
    # If you named your database differently, use that against the argument for --dbname
    ```
 
10. Run the cli by using:
    ```bash
    poetry run proxy-bot --dev
    ```

## Working
Once everything is setup, and `proxy-bot` command is invoked. 

1. You will be prompted with a list of users you can ask questions to.
   1. If they have submitted no answers, the session exits.
   2. Otherwise you are prompted to record your question. (kaldi-serve is used to transcribe the audio)

2. You get a chance to fix the transcription of your recording if kaldi-serve was not set-up, 
   an exception will be captured, allowing you to type instead.
   
3. Your query will be matched against the submissions made by the selected user and the best is returned.

An example:

![working](./assets/working.png)

When this project is completely ready, an interface would allow a user to submit question answer pairs.
This project will only be as useful as the distractions it avoids, the more frequently asked and the less frequently changing
question-answer pairs are the target of this project.

## Future works
- [ ] I had planned to build this project using Scala and Akka. So I hope for a rewrite.
- [ ] This project uses [jellyfish](https://github.com/jamesturk/jellyfish) to find the best answer to a question, more improvements can be made here.
- [ ] There needs to be more restriction on users that could be seen at a time (currently all the users are queried). I plan for region->org->team->person kind of hierarchy,
      default behaviour would be to show the members of the same team or org.
- [ ] `kaldi-serve` is no good without a model, finding or publishing a pre-trained model could help this project.
- [ ] Keeping the transcription engine itself flexible to choices, people should be able to use any transcription service.
- [ ] Currently all questions submitted by a `user` are loaded into the memory. Akka streams should help reduce this burden.
- [ ] A friendly interface for people who don't code. I have plans for an electron app and a deployed scala server.
