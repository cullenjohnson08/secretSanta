import argparse
import random
import re
import sys
from pathlib import Path
from time import sleep, strftime

from family import (
    capAmount,
    couples,
    family,
    familyLink,
    lastYear,
    serverEmail,
    serverPass,
)

FAMILY_PATH = Path(__file__).resolve().parent / "family.py"
YEAR = strftime("%Y")
SEND_DELAY_SECONDS = 20
MAX_SHUFFLE_ATTEMPTS = 10000
TEST_ALGO_DRAWS = 10
LAST_YEAR_PATTERN = re.compile(r"lastYear\s*=\s*\[[^\]]*\]", re.MULTILINE)


def generate_test_email(name):
    return (
        f"Hi, {name}!\n\n"
        "This is a test email from santaBot.\n\n"
        "Please give a thumbs up in the family group chat if you received this.\n"
    )


def generate_email_text(giver_name, receiver_name):
    return (
        f"Hi, {giver_name}!\n\n"
        "This is an automated email to inform you that you have been tasked "
        f"to buy a gift for {receiver_name}!\n\n"
        "Please remember:\n"
        "1. Keep this information strictly confidential!\n"
        f"2. Don't drastically exceed the spending limit of ${capAmount}!\n\n"
        "A list of nifty gift ideas can be found at: "
        "(make sure to put in what you want, if you haven't already!)\n"
        f"{familyLink}\n"
        "\n\nDon't be the one that ruins Chrismas this year!\n\n\n"
        "Best Wishes!\n"
        "Your friendly neighborhood santaBot"
    )


def send_mail(to_email, subject, content):
    import yagmail

    with yagmail.SMTP(serverEmail, serverPass) as yag:
        yag.send(to_email, subject, content)
    sleep(SEND_DELAY_SECONDS)


def send_test_email(person):
    send_mail(person[1], "SANTA TEST", generate_test_email(person[0]))


def send_assignment_email(giver, receiver):
    subject = f"**TOP SECRET** Your {YEAR} Secret Santa Assignment **TOP SECRET**"
    send_mail(giver[1], subject, generate_email_text(giver[0], receiver[0]))


def assignment_pairs(order):
    size = len(order)
    return [(order[i][0], order[(i + 1) % size][0]) for i in range(size)]


def is_forbidden(giver, receiver):
    if (giver, receiver) in couples or (receiver, giver) in couples:
        return True
    return (giver, receiver) in lastYear


def is_valid_draw(order):
    return all(
        not is_forbidden(giver, receiver)
        for giver, receiver in assignment_pairs(order)
    )


def draw_assignments():
    order = family[:]
    for _ in range(MAX_SHUFFLE_ATTEMPTS):
        random.shuffle(order)
        if is_valid_draw(order):
            return order
    raise RuntimeError(
        f"Could not find a valid assignment after {MAX_SHUFFLE_ATTEMPTS} shuffles"
    )


def format_last_year(pairs):
    lines = ["lastYear = ["]
    for giver, receiver in pairs:
        lines.append(f'    ("{giver}", "{receiver}"),')
    lines.append("    ]")
    return "\n".join(lines)


def write_last_year(pairs, path=FAMILY_PATH):
    family_file = Path(path)
    text = family_file.read_text()
    block = format_last_year(pairs)
    if LAST_YEAR_PATTERN.search(text):
        text = LAST_YEAR_PATTERN.sub(block, text, count=1)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    family_file.write_text(text)


def dry_run():
    total = len(family)
    print(f"Sending test emails to {total} people")
    for index, person in enumerate(family, start=1):
        print(f"Sending test email {index}/{total} to {person[0]}")
        send_test_email(person)
    print("Dry run complete")


def pair_reasons(giver, receiver):
    reasons = []
    if giver == receiver:
        reasons.append("self")
    if (giver, receiver) in couples or (receiver, giver) in couples:
        reasons.append("couple")
    if (giver, receiver) in lastYear:
        reasons.append("last year")
    return reasons


def describe_violations(pairs):
    names = [person[0] for person in family]
    givers = [giver for giver, _receiver in pairs]
    receivers = [receiver for _giver, receiver in pairs]
    violations = []
    if sorted(givers) != sorted(names):
        violations.append("givers are not a 1:1 match with the family")
    if sorted(receivers) != sorted(names):
        violations.append("receivers are not a 1:1 match with the family")
    pair_notes = []
    for giver, receiver in pairs:
        reasons = pair_reasons(giver, receiver)
        pair_notes.append((giver, receiver, reasons))
        if reasons:
            violations.append(f"{giver} -> {receiver} ({', '.join(reasons)})")
    return violations, pair_notes


def print_draw(index, pair_notes, violations):
    title = f"Draw {index}" if not violations else f"Draw {index} FAILED"
    print(title)
    for giver, receiver, reasons in pair_notes:
        suffix = f"  [{', '.join(reasons)}]" if reasons else ""
        print(f"  {giver} -> {receiver}{suffix}")
    for violation in violations:
        if " -> " not in violation:
            print(f"  {violation}")


def test_algo(draw_count=TEST_ALGO_DRAWS):
    for index in range(1, draw_count + 1):
        order = draw_assignments()
        pairs = assignment_pairs(order)
        violations, pair_notes = describe_violations(pairs)
        print_draw(index, pair_notes, violations)
        if violations:
            return False
        print("  valid")
        print()
    print(f"{draw_count}/{draw_count} valid")
    return True


def send_live():
    order = draw_assignments()
    pairs = assignment_pairs(order)
    total = len(order)
    print(f"Sending {total} assignment emails")
    rotated = order[1:] + order[:1]
    for index, (giver, receiver) in enumerate(zip(order, rotated), start=1):
        print(f"Sending assignment email {index}/{total}")
        send_assignment_email(giver, receiver)
    write_last_year(pairs)
    print("All assignment emails sent; lastYear updated in family.py")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send Secret Santa test emails or live assignments."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Send a test email to each family member with no assignment",
    )
    group.add_argument(
        "--send",
        action="store_true",
        help="Draw assignments and send live emails",
    )
    group.add_argument(
        "--test-algo",
        action="store_true",
        help="Draw 10 assignments and confirm none violate couple or last-year rules",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.dry_run:
        dry_run()
    elif args.send:
        send_live()
    elif args.test_algo:
        if not test_algo():
            sys.exit(1)


if __name__ == "__main__":
    main()
