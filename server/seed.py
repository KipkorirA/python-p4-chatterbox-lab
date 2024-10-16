#!/usr/bin/env python3

import argparse
from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

# Generate a list of usernames, ensuring "Duane" is included
usernames = [fake.first_name() for _ in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages(count):
    """Generate fake messages and add them to the database."""
    # Delete existing messages
    Message.query.delete()
    
    messages = []
    
    for _ in range(count):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    
    try:
        db.session.commit()        
        print(f"{count} messages added to the database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding messages: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate fake messages for the database.')
    parser.add_argument('--count', type=int, default=20, help='Number of messages to generate')
    args = parser.parse_args()

    with app.app_context():
        make_messages(args.count)
