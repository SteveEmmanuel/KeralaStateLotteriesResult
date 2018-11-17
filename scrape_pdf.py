import PyPDF2
import re
import os


def scrape_pdf(name):
    os.chdir(os.path.dirname(__file__))
    pdf_file = open(name, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    text = ''
    for n in range(number_of_pages):
        page = read_pdf.getPage(n)
        text = text + page.extractText()
    #print text.encode('utf-8')

    # print text
    prizes = {}

    headings = re.findall(
        r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*2301740([\w\s-]*)LOTTERY NO.([\w\s-]*)[st,nd,rd,th ]*DRAW held on ([\d\/]*) AT ([\w\s,]*)1st', text)
    first = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*1st Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)Consolation Prize',
                       text)
    prizes.update({"first": {"prize_money": first[0][0], "prizes": split_prize_number(first[0][1])}})

    consolation = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*Consolation Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)2nd',
                             text)
    prizes.update({"consolation": {"prize_money": consolation[0][0],
                                   "prizes": split_prize_number(consolation[0][1])}} )

    second = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*2nd Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)3rd', text)
    position = second[0][1].lower().find("for")
    if position!= -1:
        prizes.update({"second": {"prize_money": second[0][0], "prizes": split_prize_number(second[0][1][:position-len(second[0][1])])}})
    else:
        prizes.update({"second": {"prize_money": second[0][0], "prizes": split_prize_number(second[0][1])}})

    third = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*3rd Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)FOR', text)

    if third.__len__() == 0:
        third = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*3rd Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)4th', text)
        prizes.update({"third": {"prize_money": third[0][0], "prizes": split_prize_number(third[0][1])}})
    else:
        prizes.update({"third": {"prize_money": third[0][0], "prizes": split_prize_number(third[0][1])}})

    fourth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*4th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)5th', text)
    prizes.update({"fourth": {"prize_money": fourth[0][0], "prizes": split_prize_number(fourth[0][1])}})

    fifth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*5th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)6th', text)
    prizes.update({"fifth": {"prize_money": fifth[0][0], "prizes": split_prize_number(fifth[0][1])}})

    sixth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*6th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)7th', text)
    prizes.update({"sixth": {"prize_money": sixth[0][0], "prizes": split_prize_number(sixth[0][1])}})

    seventh = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*7th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)8th', text)
    prizes.update({"seventh": {"prize_money": seventh[0][0], "prizes": split_prize_number(seventh[0][1])}})

    eighth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*8th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)9th', text)
    if eighth.__len__() == 0:
        eighth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*8th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)The', text)
    if eighth.__len__() != 0:
        prizes.update({"eighth": {"prize_money": eighth[0][0], "prizes": split_prize_number(eighth[0][1])}})

    ninth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*9th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)10th', text)
    if ninth.__len__() == 0:
        ninth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*9th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)The', text)
    if ninth.__len__() != 0:
        prizes.update({"ninth": {"prize_money": ninth[0][0], "prizes": split_prize_number(ninth[0][1])}})

    tenth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*10th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)11th', text)
    if tenth.__len__() == 0:
        tenth = re.findall(r'[a-zA-Z0-9!@#$&()\\-`.+,/\"]*10th Prize[-\s]*Rs[.:\s]*([\d,]*)/-([\w\s\(\)]*)the', text)
    if tenth.__len__() != 0:
        prizes.update({"tenth": {"prize_money": tenth[0][0], "prizes": split_prize_number(tenth[0][1])}})

    '''print headings
    print "first ", first
    print "consolation ", consolation
    print "second ", second
    print "third ", third
    print "fourth ", fourth
    print "fifth ", fifth
    print "sixth ", sixth
    print "seventh ", seventh
    print "eighth ", eighth
    print "ninth ", ninth
    print "tenth ", tenth'''

    details = {}
    details.update({"info": {"name": headings[0][0], "series": headings[0][1]
                            , "date": headings[0][2], "location": headings[0][3]}, "prizes": prizes})
    return details


def split_by_n(line, n):
    return [line[i:i + n] for i in range(0, len(line), n)]

def split_prize_number(prizes_string):
    prizes_string = prizes_string.replace(' ', '')
    if re.search('[()]', prizes_string) is not None:
        split_prizes_list = re.findall(r'([a-zA-Z]*[0-9]*\(+[a-zA-Z]*\)+)', prizes_string)
    elif re.search('[a-zA-Z]', prizes_string) is not None:
        split_prizes_list = re.findall(r'([a-zA-Z]*[0-9]*)', prizes_string)
    else:
        split_prizes_list = split_by_n(prizes_string, 4)
    return split_prizes_list
