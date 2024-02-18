from controller.controller import session, Media, Category

# movies_to_add = [{'plan': 'Basic', 'name': 'Terminator 2: Judgment Day', 'category': 'Action'},
#                  {'plan': 'Regular', 'name': 'The Matrix', 'category': 'Action'},
#                  {'plan': 'Premium', 'name': 'Batman The Dark Knight', 'category': 'Action'},
#                  {'plan': 'Regular', 'name': 'John Wick', 'category': 'Action'},
#                  {'plan': 'Basic', 'name': 'Gladiator', 'category': 'Action'},]

# movies_to_add = [{'plan': 'Basic', 'name': 'Blade Runner 2049', 'category': 'Science Fiction'},
#                  {'plan': 'Premium', 'name': 'Interstellar ', 'category': 'Science Fiction'},
#                  {'plan': 'Basic', 'name': 'The Martian', 'category': 'Science Fiction'},]

# movies_to_add = [{'plan': 'Basic', 'name': 'The Grand Budapest Hotel', 'category': 'Comedy'},
#                  {'plan': 'Basic', 'name': 'Bridesmaids', 'category': 'Comedy'},
#                  {'plan': 'Premium', 'name': 'The Hangover', 'category': 'Comedy'},
#                  {'plan': 'Regular', 'name': 'Superbad', 'category': 'Comedy'},
#                  {'plan': 'Premium', 'name': 'American Pie', 'category': 'Comedy'},]

# movies_to_add = [{'plan': 'Regular', 'name': 'The Conjuring', 'category': 'Horror'},
#                  {'plan': 'Basic', 'name': 'Hereditary', 'category': 'Horror'},
#                  {'plan': 'Premium', 'name': 'The Exorcism of Emily Rose', 'category': 'Horror'},
#                  {'plan': 'Basic', 'name': 'Supernatural', 'category': 'Horror'}]

# movies_to_add = [{'plan': 'Premium', 'name': 'The Lord of the Rings', 'category': 'Adventure'},
#                  {'plan': 'Basic', 'name': 'Jurassic Park', 'category': 'Adventure'},
#                  {'plan': 'Regular', 'name': 'Pirates of the Caribbean', 'category': 'Adventure'},
#                  {'plan': 'Premium3', 'name': 'Harry Potter', 'category': 'Adventure'},
#                  {'plan': 'Basic', 'name': 'The Jungle Book', 'category': 'Adventure'},]

# [session.add(Media(name=movie["name"],
#                    plan=movie["plan"],
#                    category=movie["category"])) for movie in movies_to_add]

# categories = ['Adventure', 'Comedy', 'Horror', 'Action', 'Science Fiction']
# [session.add(Category(name=line)) for line in categories]


# session.commit()
# session.close()