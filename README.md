# secretSanta
#### A script to automate a secret santa draw

## Create a family.py that contains:

Copy `exampleFamily.py` to `family.py` and fill in your details. `family.py` is gitignored so names, emails, passwords, and last year's assignments are not pushed to GitHub.

Do not put a year in `family.py`. The script uses the current calendar year in email subjects.

+ **_family_** - A list of tuples(string,string) with the name and email of each family member. _ex: ("name", "email address")_

+ **_couples_** - A list of tuples(string,string) that contains couples that you don't want to get each other, in either direction. _ex: ("mom", "dad")_

+ **_lastYear_** - A list of tuples(string,string) of last year's giver and receiver. A giver will not be assigned the same receiver two years in a row. This is one-way: `("mom", "timmy")` means mom got timmy last year, so mom cannot get timmy this year, but timmy can get mom. After a successful `--send`, this list is overwritten with this year's assignments.

+ **_capAmount_** -  An integer containing the max amount to be spent on each person.

+ **_serverEmail_** - A string containing the email you want assignments to be sent from.

+ **_serverPass_** - A string containing the password for that email address. For Gmail this should be an app password.

+ **_familyLink_** -  A string containing the link to a shared document with your family's gift ideas and links. Included in `--dry-run`, `--test-email`, and `--send` emails.

### Please reference exampleFamily.py for a template

## Run

```
python santa.py
python santa.py --dry-run
python santa.py --send
python santa.py --test-algo
python santa.py --test-email NAME
```

These flags are mutually exclusive. Running with no flags prints usage and exits.

`--dry-run` sends a test email to each real address in `family`. It does not draw or include an assignment. The subject is `SANTA TEST` plus the current year (for example `SANTA TEST 2026`). The body asks people to thumbs-up the family group chat if they received it, and to add gift ideas to the wish list at `familyLink`. There is a 20 second delay between emails.

`--test-email NAME` sends that same test email to one family member. `NAME` must match a name in `family` (case-insensitive).

`--send` draws a circular assignment that avoids couples and last year's pairs, emails everyone, then writes this year's pairs into `lastYear` in `family.py`. It does not print who got whom. There is a 20 second delay between emails.

`--test-algo` draws 10 assignments with couple and last-year checking, prints each giver→receiver map, and confirms none break the rules. It does not send email or write `family.py`. A failed draw is printed in full and the process exits non-zero.

##### This currently works with gmail as of November 2026
