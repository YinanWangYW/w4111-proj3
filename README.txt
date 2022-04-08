account:yw3692

way to git pull:
cd w4111-proj3
git pull
USERNAME:YinanWangYW
PASSWORD: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


URL external linkage http://34.148.165.149:8111/

"":YinanWangYW

vertual circumstance:
source ../yw3692/.virtualenvs/dbproj/bin/activate PTSQL:
psql -U yw3692 -h 35.211.155.104 -d proj1part2
PASSWORD:6367

parts:
We expected to finish several parts in Project1.3:
· Implement functions of user register, log in, log out.
· Users can click links on webpage to see what kinds of diet-plan and fitness-plan we provide.
· Diet-plans contain some food and expected input calorie, Fitness-plans contain body parts, exercise moves, and some kind of musics. Users can select some certain plans according to their favor on these features.
· Users can select choose when to exercise on their own. Also, they can upload their actual calorie input and consumption and can get small tips from administration. 

All functions described in part1.3 are all finished.

New functions: we provide some coaches and their personal info, as well as what fitness plans they provide. Users can choose their favorite coaches.


Two web pages:
1. Register page and login page. Register page is used to register, user can upload their personal info. When finishing register, these data will be insert to database. Log in page is used to login. At this time we will select data from database and use logical relationship to judge repetition. Register and login need some complicated judgement, and implement these complicated functions are quiet interesting.
2. Dashboard page. This page is the main page which provides some main informations and can choose to make their own plans. In this page, user need to type to select certain plans, which means we will insert data into database. Also linking to concrate plan pages, we will show users the plan information, which means we will select data from database. This page is interesting because it contains a lot of information where users need to type and also linking to other pages.