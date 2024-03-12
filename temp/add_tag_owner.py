import json
from random import choice, randint

# Function to create fixture data for Tags
def create_tag_fixture(name, pk):
    return {
        "model": "gpts.tags",
        "pk": pk,
        "fields": {
            "name": name
        }
    }

# Function to create fixture data for Owners
def create_owner_fixture(slug, pk):
    return {
        "model": "gpts.owner",
        "pk": pk,
        "fields": {
            "slug": slug
        }
    }

# Fixture data for tags
tags_fixture_data = []

# Tags names
tag_names = ["AI", "Machine Learning", "Natural Language Processing", "Deep Learning", "Chatbot", "Virtual Assistant", "Data Science", "Neural Networks", "Artificial Intelligence", "Python"]

# Generate fixture data for tags
for pk, name in enumerate(tag_names, start=1):
    tag_fixture = create_tag_fixture(name, pk)
    tags_fixture_data.append(tag_fixture)

# Dump fixture data for tags to a file
with open("tags_fixture.json", "w") as f:
    json.dump(tags_fixture_data, f, indent=4)

# Fixture data for owners
owners_fixture_data = []

# Owners names
owner_names = ["Google", "Apple", "Facebook", "Amazon", "Microsoft", "IBM", "Oracle", "Intel", "Cisco", "NVIDIA"]

# Generate fixture data for owners
for pk, name in enumerate(owner_names, start=1):
    owner_fixture = create_owner_fixture(name, pk)
    owners_fixture_data.append(owner_fixture)

# Dump fixture data for owners to a file
with open("owners_fixture.json", "w") as f:
    json.dump(owners_fixture_data, f, indent=4)
