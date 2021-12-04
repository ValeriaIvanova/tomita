import nltk
from nltk.corpus import wordnet as wn

def change(word):
    try:
        synonym = wn.synsets(word)[0].lemmas()[0].name()
        if word == synonym:
            synonym = wn.synsets(word)[0].lemmas()[1].name()
        if synonym != None:
            print("word: " + str(word))
            print("synonym: " + str(synonym))
            word = str(synonym)
        return word
    except:
        return word


def main():
    nltk.download('wordnet')
    chars = '.,!?:\"\''
    resText = []

    with open("input.txt", encoding='utf-8') as f:
        for line in f.readlines():
            new_l = line
            print(line)
            for ch in chars:
                line = line.replace(ch, '')
            for word in line.split():
                synonym = change(word)
                if synonym != None:
                    new_l = new_l.replace(word, synonym)

            resText.append(new_l)

    with open("output.txt", 'w', encoding='utf-8') as f:
        f.writelines(resText)
        print(resText)


if __name__ == '__main__':
    main()