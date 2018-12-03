from app import db
from app import Lottery
from sys import argv

'''logging.basicConfig(
    filename="/home/steveisredatw/task.log",
    level=logging.DEBUG
)'''
base_url = "https://www.keralastatelotteriesresult.in/result/"


def generate_post(lotteries):
    posts = ''
    for lottery in lotteries:
        url = base_url + str(lottery.id)
        name = lottery.name
        series = lottery.series
        date = lottery.date.strftime('%a, %d/%m/%Y')
        post = name + "(" + series + ")" + " results announced on " + date + ". Check at " + url + "\n\n"
        posts = posts + post
    print(posts)


def main():
    lotteries = db.session.query(Lottery).order_by(Lottery.date.desc())
    number = int(argv[1])
    if number == -1:
        pass  # get all posts
    if number > 0:
        lotteries = lotteries.limit(number)
    generate_post(lotteries)


if __name__ == "__main__":
    main()
