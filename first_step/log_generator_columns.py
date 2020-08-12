import csv
import random

from faker import Faker

views = open("Views.csv", "w")
reviews = open("Reviews.csv", "w")
catalog = open("Catalog.csv", "w")

w_views = csv.writer(views)
w_reviews = csv.writer(reviews)
w_catalog = csv.writer(catalog)

w_views.writerow(('item_id', 'timestamp', 'device_type', 'device_id', 'user_ip'))
w_reviews.writerow(
    ('item_id', 'timestamp', 'device_type', 'device_id', 'user_ip', 'review_title', 'review_text', 'review_stars'))
w_catalog.writerow(('item_id', 'title', 'description', 'category'))

for i in range(1500):
    fake = Faker()

    review_text = random.choice(['great', 'very good', 'good', 'bad', 'very bad', 'super', 'awesome', 'awful', ''])

    device_type = random.choice(
        ['device1', 'device2', 'device3', 'device4', 'device5', 'device6', 'device7', 'device8', 'device9', 'device10',
         'device11', 'device12', 'device13', 'device14', 'device15', 'device16', 'device17', 'device18', 'device19',
         'device20'])


    def create_review_stars(argument):
        switcher = {
            'very bad': '1',
            'bad': '2',
            'good': '3',
            'very good': '4',
            'great': '5'
        }
        return switcher.get(argument, "Review does not exist!")


    def create_device_id(argument):
        switcher = {
            'device1': '1d',
            'device2': '2d',
            'device3': '3d',
            'device4': '4d',
            'device5': '5d',
            'device6': '6d',
            'device7': '7d',
            'device8': '8d',
            'device9': '9d',
            'device10': '10d',
            'device11': '11d',
            'device12': '12d',
            'device13': '13d',
            'device14': '14d',
            'device15': '15d',
            'device16': '16d',
            'device17': '17d',
            'device18': '18d',
            'device19': '19d',
            'device20': '20d'
        }
        return switcher.get(argument, "Device does not exist!")


    user_ip = fake.ipv4()

    views_row = ('{}i'.format(random.choice(range(1, 1300))),
                 fake.date_time_ad(tzinfo=None, start_datetime='-30w', end_datetime='now'), device_type,
                 create_device_id(device_type), user_ip)
    w_views.writerow(views_row)

    reviews_row = ('{}i'.format(random.choice(range(1, 1300))).format(i + 1),
                   fake.date_time_ad(tzinfo=None, start_datetime='-30w', end_datetime='now'), device_type,
                   create_device_id(device_type), user_ip,
                   random.choice(
                       ['review1', 'review2', 'review3', 'review4', 'review5', 'review6', 'review7', 'review8',
                        'review9', 'review10', '']), review_text,
                   create_review_stars(review_text))
    w_reviews.writerow(reviews_row)

    catalog_row = (
    '{}i'.format(random.choice(range(1, 1300))).format(i + 1), 'title{}'.format(random.choice(range(1, 1300))),
    'description{}'.format(random.choice(range(1, 1300))), 'category{}'.format(random.choice(range(1, 50))))
    w_catalog.writerow(catalog_row)

views.close()
reviews.close()
catalog.close()
