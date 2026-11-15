# secretSanta
#### A script to automate a secret santa draw

## Create a family.py that contains:

Copy `exampleFamily.py` to `family.py` and fill in your details. `family.py` is gitignored so names, emails, passwords, and last year's assignments are not pushed to GitHub.

+ **_family_** - A list of tuples(string,string) with the name and email of each family member. _ex: ("name", "email address")_

+ **_couples_** - A list of tuples(string,string) that contains couples that you don't want to get each other. _ex: ("mom", "dad")_

+ **_lastYear_** - A list of tuples(string,string) of last year's giver and receiver. A giver will not be assigned the same receiver two years in a row. This is one-way: `("mom", "timmy")` means mom got timmy last year, so mom cannot get timmy this year, but timmy can get mom. After a successful `--send`, this list is overwritten with this year's assignments.

+ **_capAmount_** -  An integer containing the max amount to be spent on each person.

+ **_serverEmail_** - A string containing the email you want assignments to be sent from.

+ **_serverPass_** - A string containing the password for that email address.

+ **_familyLink_** -  A string containing the link to a shared document with your family's gift ideas and links.

### Please reference exampleFamily.py for a template

## Run

```
python santa.py --dry-run
python santa.py --send
python santa.py --test-algo
```

`--dry-run` sends a test email to each real address in `family`. It does not draw or include an assignment. Ask people to thumbs-up the family group chat when it arrives.

`--send` draws a circular assignment that avoids couples and last year's pairs, emails everyone, then writes this year's pairs into `lastYear` in `family.py`. Running with no flags prints usage and exits.

`--test-algo` draws 10 assignments with couple and last-year checking, prints each giver→receiver map, and confirms none break the rules. It does not send email or write `family.py`. A failed draw is printed in full and the process exits non-zero.

There is a 20 second delay between emails.

##### This currently works with gmail as of November 2023
