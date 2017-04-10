from __future__ import print_function
import os
import sys
import re
import codecs


AuthorRegex = re.compile(r'(?<=<META NAME="AUTOR" CONTENT=").+(?=">)')
TypeRegex = re.compile(r'(?<=<META NAME="DZIAL" CONTENT=").+(?=">)')
KeywordsRegex = re.compile(r'(?<=<META NAME="KLUCZOWE_\d" CONTENT=").+(?=">)')
SentenceRegex = re.compile(r'(([a-zA-Z]{4}| +)(\.|!|\?)+|(<.+>)+\n)')
ShortcutRegex = re.compile(r'\s[a-zA-Z]{1,3}\.')
IntsRegex = re.compile(r'(\b-?(3276[0-7]|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9]|[1-2][0-9][0-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9]|[0-9])|-32768\b)(?![\s\S]*\1)')
FloatRegex = re.compile(r'\s-?(([1-9]+\d*\.\d*)|((([1-9]+\d*)|()|(0))\.\d+([Ee]\+\d+)?))\s')
EmailRegex = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.([a-zA-Z0-9-]|(?<!\.)\.)+\b')
DataRegex = re.compile(r'(\b(?P<Year>\d{4})(?P<Separator>-|\/|\.)(?P<Months>(?P<MonthFor31>'
                       r'((0[13578])|(1[02])))|(?P<MonthFor30>((0[469])|(11)))|(?P<Feb>02))'
					   r'(?P=Separator)(?P<Days>(?(MonthFor31)(0[1-9]|[12][0-9]|3[01])|'
					   r'(?(MonthFor30)(0[1-9]|[12][0-9]|30)|(?(Feb)(0[1-9]|[12][0-9])))))|'
					   r'((?P<DDays>(?P<D30>(0[1-9]|[12][0-9]|30)|(?P<D31>0[1-9]|[12][0-9]|31)))'
					   r'(?P<SSeparator>-|\/|\.)(?P<MMonths>(?(D31)(0[13578]|1[02])|(?(D30)'
					   r'(0[13456789]|1[0-2])|(0[1-9]|1[0-2]))))(?P=SSeparator)(?P<YYear>\d{4})\b))'
					   r'(?![\s\S]*(((?P=YYear)(?P<SSSeparator>-|\/|\.)(?P=MMonths)(?P=SSSeparator)'
					   r'(?P=DDays))|((?P=Days)(?P<SSSSeparator>-|\/|\.)(?P=Months)(?P=SSSSeparator)'
					   r'(?P=Year))|((?P=Year)(?P<SSSSSeparator>-|\/|\.)(?P=Months)(?P=SSSSSeparator)'
					   r'(?P=Days))|((?P=DDays)(?P<SSSSSSeparator>-|\/|\.)(?P=MMonths)(?P=SSSSSSeparator)(?P=YYear))))')

FindInsideRegex = re.compile(r'(?<=<P>).*(?=</P>)', re.DOTALL)


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()
    cutted_content = FindInsideRegex.search(content).group()

    print("nazwa pliku:", filepath)
    print("autor:", findWithRegex(AuthorRegex, content))
    print("dzial:", findWithRegex(TypeRegex, content))
    print("slowa kluczowe:", findWithRegex(KeywordsRegex, content))
    print("liczba zdan:", countWithRegex(SentenceRegex, cutted_content))
    print("liczba skrotow:", countWithRegex(ShortcutRegex, cutted_content))
    print("liczba liczb calkowitych z zakresu int:", countWithRegex(IntsRegex, cutted_content))
    print("liczba liczb zmiennoprzecinkowych:", countWithRegex(FloatRegex, cutted_content))
    print("liczba dat:", countWithRegex(DataRegex, cutted_content))
    print("liczba adresow email:", countWithRegex(EmailRegex, cutted_content))
    print("\n")

    fp.close()

def makeList(list):
    return ', '.join(list)


def findWithRegex(Regex, text):
    return makeList(Regex.findall(text))


def countWithRegex(Regex, text):
    return len(Regex.findall(text))


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)


