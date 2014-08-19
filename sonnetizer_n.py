from sys import argv
import random
import re
import nltk
import roman
import operator
from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import LidstoneProbDist

if len(argv) == 6:
    script, book, rhyme_scheme, poem_count, output_format, show_diagnostics = argv
elif len(argv) == 5:
    script, book, rhyme_scheme, poem_count, output_format = argv
    show_diagnostics = 'y'
elif len(argv) == 4:
    script, book, rhyme_scheme, poem_count = argv
    output_format = 'pt'
    show_diagnostics = 'y'
elif len(argv) == 3:
    script, book, rhyme_scheme = argv
    poem_count = '10'
    output_format = 'pt'
    show_diagnostics = 'y'
else:
    print "invalid input arguments"

e = cmudict.entries()
d = cmudict.dict()

st = SnowballStemmer("english")

banned_end_words = ['the', 'a', 'an', 'at', 'been', 'in', 'of', 'to', 'by', 'my', 'too', 'not', 
                    'and', 'but', 'or', 'than', 'then', 'no', 'o', 'for', 'so', 'which', 'their', 
                    'on', 'your', 'as', 'has', 'what', 'is', 'nor', 'i', 'that', 'am', 'be', 'and',
                    'with', 'it', 'is', 'will', 'in', 'its', 'of', 'we', 'was', 'were', 'have',
                    'you', 'do', 'had', 'whose', 'while', 'because']

banned_word_combos = [['the', 'and', 'the'], ['at', 'to'], ['around', 'about'], ['the', 'all', 'the'], ['the', 'of', 'the']]

if show_diagnostics.lower() == 'y':
    print "importing source text..."
f = open(book)
if show_diagnostics.lower() == 'y':
    print "reading source text..."
t = f.read()
if show_diagnostics.lower() == 'y':
    print "tokenizing words..."
w = nltk.word_tokenize(t)


#print "pos tagging book..."
#pos = nltk.pos_tag(words)


def remove_ml_words():
    if show_diagnostics.lower() == 'y':
        print "distilling to nouns and verbs..."
    nv = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    signal = []
    for (i, j) in pos:
        for x in nv:
            if j == x and not i in ['is', 'are', 'were', 'to', 'be', 'has', 'have', 'will', 'its']:
                signal.append(i)
            else:
                pass
    return signal
                
#w = remove_ml_words() 


def make_word_list():
    if show_diagnostics.lower() == 'y':
        print "making word list..."
    word_list = []
    for i in w:
        try:
            d[i.lower()]
        except KeyError:
            pass
        else:
            if i.lower() == "'s":
                pass
            elif i[-1] == ".":
                pass
            else:
                word_list.append((i.lower(), d[i.lower()][0]))
    return word_list
    
word_list = make_word_list()


def valid_words():
    if show_diagnostics.lower() == 'y':
        print "extracting words from word list..."
    vw = []
    for (x, y) in word_list:
        vw.append(x)
    return vw
    
vw = valid_words()
vw_u = list(set(vw))


def unique(s):
    u = []
    for x in s:
        if x not in u:
            u.append(x)
        else:
            pass
    return u
    
word_list_u = unique(word_list)


def in_pdict(word):
    try:
        d[word]
    except KeyError:
        return False
    else:
        return True


def sylcount(s):
    try:
        d[s]
    except KeyError:
        return None
    else:
        if len(d[s]) <= 1:
            sj = ''.join(d[s][0])
            sl = re.split('0|1|2', sj)
            return len(sl) - 1
        else:
            sj0 = ''.join(d[s][0])
            sl0 = re.split('0|1|2', sj0)
            sj1 = ''.join(d[s][1])
            sl1 = re.split('0|1|2', sj1)
            if len(sl1) < len(sl0):
                return len(sl1) - 1
            else:
                return len(sl0) - 1
        
        
def line_sylcount(line):
    count = 0
    for word in line:
        count += sylcount(word)
    return count
    

def meter(word):
    pron = d[word]
    m1 = []
    m2 = []
    mx = []
    if len(pron) == 1:
        for i in pron[0]:
            if '0' in i:
                m1.append(0)
            elif '1' in i:
                m1.append(1)
            elif '2' in i:
                m1.append(2)
            else:
                pass
        mx = [m1]
    elif len(pron) >= 2:
        for i in pron[0]:
            if '0' in i:
                m1.append(0)
            elif '1' in i:
                m1.append(1)
            elif '2' in i:
                m1.append(2)
            else:
                pass
        for i in pron[1]:
            if '0' in i:
                m2.append(0)
            elif '1' in i:
                m2.append(1)
            elif '2' in i:
                m2.append(2)
            else:
                pass
        mx = [m1, m2]
    m = []
    if len(mx) == 1:
        w0 = reduce(operator.mul, mx[0], 1)
        if w0 >= 2:
            for i in mx[0]:
                if i == 1:
                    m.append('u')
                elif i == 2:
                    m.append('s')
        elif w0 == 1:
            for i in mx[0]:
                m.append('s')
        elif w0 == 0:
            for i in mx[0]:
                if i == 0:
                    m.append('u')
                elif i == 1 or i == 2:
                    m.append('s')
    elif len(mx) == 2:
        w0 = reduce(operator.mul, mx[0], 1)
        w1 = reduce(operator.mul, mx[1], 1)
        if w0 >= 2 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if i * j == 1:
                    m.append('u')
                elif i * j == 4:
                    m.append('s')
                elif i * j == 2:
                    m.append('x')
        elif w0 == 1 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                m.append('s')
        elif w0 == 0 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if i == j and i * j >= 1:
                    m.append('s')
                elif i != j and i * j == 0:
                    m.append('x')
                elif i == j and i * j == 0:
                    m.append('u')
        elif w0 >= 2 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 1 and j == 0:
                    m.append('u')
                elif i == 2 and j == 0:
                    m.append('x')
                elif i == 1 and j == 1:
                    m.append('x')
                elif i == 1 and j == 2:
                    m.append('x')
                elif i == 2 and j == 1:
                    m.append('s')
                elif i == 2 and j == 2:
                    m.append('s')
        elif w0 == 0 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 0 and j == 1:
                    m.append('u')
                elif i == 0 and j == 2:
                    m.append('x')
                elif i == 1 and j == 1:
                    m.append('x')
                elif i == 2 and j == 1:
                    m.append('x')
                elif i == 1 and j == 2:
                    m.append('s')
                elif i == 2 and j == 2:
                    m.append('s')
        elif w0 == 1 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if j == 1:
                    m.append('x')
                elif j == 2:
                    m.append('s')
        elif w0 >= 2 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 1:
                    m.append('x')
                elif i == 2:
                    m.append('s')
        elif w0 == 1 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if j == 0:
                    m.append('x')
                elif j == 1:
                    m.append('s')
                elif j == 2:
                    m.append('s')
        elif w0 == 0 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 0:
                    m.append('x')
                elif i == 1:
                    m.append('s')
                elif i == 2:
                    m.append('s')       
    return m


def strip_numbers(x):
    xj = '.'.join(x)
    xl = re.split('0|1|2', xj)
    xjx = ''.join(xl)
    xlx = xjx.split('.')
    return xlx


def get_pron(word):
    if not in_pdict(word):
        pron = None
    else:
        if len(d[word]) <= 1:
            pron = d[word][0]
        else:
            p0 = d[word][0]
            p1 = d[word][1]
            sj0 = ''.join(p0)
            sl0 = re.split('0|1|2', sj0)
            sj1 = ''.join(p1)
            sl1 = re.split('0|1|2', sj1)
            if len(sl1) < len(sl0):
                pron = p1
            else:
                pron = p0
    return pron


def last_stressed_vowel(word):
    pron = get_pron(word)
    mtr = meter(word)
    vowel_index = []
    if len(mtr) == 1:
        lsv = -1
    elif mtr[-1] == 's' or mtr[-1] == 'x':
        lsv = -1
    elif mtr[-2] == 's' or mtr[-2] == 'x':
        lsv = -2
    elif mtr[-3] == 's' or mtr[-3] == 'x':
        lsv = -3
    elif mtr[-4] == 's' or mtr[-4] == 'x':
        lsv = -4
    elif mtr[-5] == 's' or mtr[-5] == 'x':
        lsv = -5
    elif mtr[-6] == 's' or mtr[-6] == 'x':
        lsv = -6
    elif mtr[-7] == 's' or mtr[-7] == 'x':
        lsv = -7
    elif mtr[-8] == 's' or mtr[-8] == 'x':
        lsv = -8
    elif mtr[-9] == 's' or mtr[-9] == 'x':
        lsv = -9
    elif mtr[-10] == 's' or mtr[-10] == 'x':
        lsv = -10
    else:
        lsv = -1
    for i in pron:
        if '0' in i or '1' in i or '2' in i:
            vowel_index.append(pron.index(i))
        else:
            continue
    return vowel_index[lsv]


def rhyme_finder(word):
    rhyming_words = []
    pron = get_pron(word)
    pron = strip_numbers(pron)
    lsv = last_stressed_vowel(word)
    rhyme_part = pron[lsv:]
    lrp = len(rhyme_part) * -1
    for (x, y) in word_list_u:
        ps = strip_numbers(y)
        if ps[lrp:] == rhyme_part and ps[lrp-1:] != pron[lsv-1:]:
            rhyming_words.append(x)
        else:
            pass
    rw = [i for i in rhyming_words if not i == word]
    rw2 = [j for j in rw if not j in banned_end_words]
    return rw2


def contains_rhyme(rs):
    rs_list = [i for i in rs]
    letters = []
    for x in rs_list:
        try:
            int(x)
        except ValueError:
            letters.append(x)
        else:
            pass
    letters_u = list(set(letters))
    if len(letters_u) == len(letters):
        return False
    else:
        return True


if contains_rhyme(rhyme_scheme) or "natural" in rhyme_scheme.lower():
    if show_diagnostics.lower() == 'y':
        print "compiling rhymes..."
    rhyme_dict = {}
    rhyme_counts = []
    for word in vw_u:
        rhymes = rhyme_finder(word)
        rhyme_dict[word] = rhymes
        rhyme_counts.append(len(rhymes))
    rhyme_freq = {}
    for i in range(max(rhyme_counts)+1):
        rhyme_freq[i] = []
    for word in vw_u:
        rhyme_freq[len(rhyme_dict[word])].append(word)
else:
    pass
    

if show_diagnostics.lower() == 'y':
    print "building content model..."
estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
content_model = nltk.NgramModel(3, vw, estimator=estimator)


def sw():
    sw1 = random.randint(0, len(vw) - 2)
    return [vw[sw1], vw[sw1+1]]


def generate_line(prior_words):
    line = []
    sc = 0
    word_y = content_model.generate(1, prior_words)
    word_y = word_y[-1]
    line += [prior_words[-1], word_y]
    sc += sylcount(word_y)
    # maybe tweak this number...
    while sc < 10:
        word_z = content_model.generate(1, line[-2:])
        word_z = word_z[-1]
        line.append(word_z)
        sc += sylcount(word_z)
    return line[1:]


def generate_sonnet(starting_words):
    sonnet = []
    lx = generate_line(starting_words)
    sonnet.append(lx)
    if "natural" in rhyme_scheme:
        rs = rhyme_scheme.split('_')
        line_count = int(rs[1])
    else:
        line_count = len(rhyme_scheme)
    for i in range(line_count-1):
        ly = generate_line(lx[-2:])
        sonnet.append(ly)
        lx = ly
    return sonnet


def plagiarism_check(sonnet):
    for line in sonnet[:]:
        if any(line == vw[i:i+len(line)] for i in xrange(len(vw) - len(line) + 1)):
            sonnet.remove(line)
        else:
            pass
    return sonnet


def line_syn_replace(line):
    pos = nltk.pos_tag(line)
    nvaa = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 
            'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']
    candidates = []
    for h in range(len(pos)):
        if pos[h][1] in nvaa:
            candidates.append(h)
        else:
            pass
    synset_count_list = []
    lemma_list = []
    for n in candidates:
        ss = wn.synsets(line[n])
        synset_count_list.append(len(ss))
        lemmas = []
        for i in ss:
            lemmas += i.lemma_names
        lemmas = list(set(lemmas))
        for lem in lemmas[:]:
            if st.stem(line[n]) == st.stem(lem):
                lemmas.remove(lem)
            else:
                pass
        lemma_list.append(lemmas)
    pos_ss_count = [synset_count_list[j] for j in range(len(candidates)) if synset_count_list[j] > 0 and lemma_list[j] != []]
    if pos_ss_count == []:
        synonym = "asdfjkl"
    else:
        min_pos_ss_count = min(pos_ss_count)
        for k in range(len(candidates)):
            if synset_count_list[k] == min_pos_ss_count and lemma_list[k] != []:
                word_index = candidates[k]
                syn_candidates = lemma_list[k]
                break
            else:
                pass
        for l in range(len(syn_candidates)):
            syn_candidates[l] = syn_candidates[l].lower()
            if '_' in syn_candidates[l]:
                tp = syn_candidates[l].split('_')
                tj = ' '.join(tp)
                syn_candidates[l] = tj
            else:
                pass
        synonym = random.choice(syn_candidates)
        line[word_index] = synonym
    
    # if natural line breaks desired, update rhyming dicts...
    
    if "natural" in rhyme_scheme.lower():
        if ' ' in synonym:
            synonym = synonym.split(' ')
        else:
            synonym = [synonym]
        for w in synonym:
            if in_pdict(w):
                rhymes = rhyme_finder(w)
                rhyme_dict[w] = rhymes
                if len(rhymes) > max(rhyme_counts):
                    rhyme_counts.append(len(rhymes))
                    rhyme_freq[len(rhymes)] = [w]
                else:
                    rhyme_counts.append(len(rhymes))
                    rhyme_freq[len(rhymes)].append(w)
            else:
                rhyme_dict[w] = []
                if 0 in rhyme_counts:
                    rhyme_counts.append(0)
                    rhyme_freq[0].append(w)
                else:
                    rhyme_counts.append(0)
                    rhyme_freq[0] = [w]
    
    return line


def plagiarism_syn_replace(sonnet):
    for i in range(len(sonnet)):
        if any(sonnet[i] == vw[j:j+len(sonnet[i])] for j in xrange(len(vw) - len(sonnet[i]) + 1)):
            sonnet[i] = line_syn_replace(sonnet[i])
        else:
            pass
    return sonnet


def end_words(sonnet):
    for i in range(len(sonnet)-1):
        while sonnet[i][-1] in banned_end_words:
            if any([sonnet[i][-1], sonnet[i+1][0]] == vw[j:j+2] for j in xrange(len(vw)-1)):
                break
            else:
                sonnet[i] = sonnet[i][:-1]
        else:
            pass
    return sonnet


def line_rhymer(sonnet, line_numbers):
    origin_word = sonnet[line_numbers[0]][-1]
    candidate_count = len(line_numbers) - 1
    if len(rhyme_dict[origin_word]) >= candidate_count:
        pass
    else:
        new_owc = []
        for i in range(candidate_count, max(rhyme_counts)+1):
            new_owc += rhyme_freq[i]
        origin_word = random.choice(new_owc)
        sonnet[line_numbers[0]][-1] = origin_word
    rhyming_words = random.sample(rhyme_dict[origin_word], candidate_count)
    for i in range(candidate_count):
        sonnet[line_numbers[i+1]][-1] = rhyming_words[i]
    return sonnet


def line_repeater(sonnet, line_numbers):
    origin_line = sonnet[line_numbers[0]]
    for i in line_numbers[1:]:
        sonnet[i] = origin_line
    return sonnet


def rhymer(sonnet):
    rs_list = [i for i in rhyme_scheme]
    rs_u = unique(rs_list)
    rs_u_n = []
    rs_u_l = []
    for des in rs_u:
        try:
            int(des)
        except ValueError:
            rs_u_l.append(des)
        else:
            rs_u_n.append(des)
    rs_n_loc = [[] for i in rs_u_n]
    locations = [[] for i in rs_u_l]
    for i in range(len(rs_u_l)):
        for j in range(len(rs_list)):
            if rs_u_l[i] == rs_list[j]:
                locations[i].append(j)
            else:
                pass
    for n in range(len(rs_u_n)):
        for m in range(len(rs_list)):
            if rs_u_n[n] == rs_list[m]:
                rs_n_loc[n].append(m)
            else:
                pass
    for x in locations:
        if len(x) <= 1:
            pass
        else:
            sonnet = line_rhymer(sonnet, x)
    for y in rs_n_loc:
        if len(y) <= 1:
            pass
        else:
            sonnet = line_repeater(sonnet, y)
    return sonnet


def slant_rhyme_loc(word, word_set):
    loc = []
    pron = get_pron(word)
    if pron == None:
        pass
    else:
        pron = strip_numbers(pron)
        for i in range(len(word_set)):
            ipron = get_pron(word_set[i])
            if ipron == None:
                pass
            else:
                ipron = strip_numbers(ipron)
                if pron == ipron:
                    pass
                else:
                    if len(pron) == 1:
                        if any(pron[0] == ipron[j] for j in xrange(len(ipron))):
                            loc.append(i)
                        else:
                            pass
                    elif len(ipron) == 1:
                        if any(ipron[0] == pron[j] for j in xrange(len(pron))):
                            loc.append(i)
                        else:
                            pass
                    else:
                        for x in range(len(pron)-1):
                            for y in range(len(ipron)-1):
                                if pron[x] == ipron[y] and pron[x+1] == ipron[y+1]:
                                    loc.append(i)
                                else:
                                    pass
        loc = list(set(loc))
    return loc


def rhyme_loc(word, word_set):
    loc = []
    rhyming_words = rhyme_dict[word]
    for i in range(len(word_set)):
        if word_set[i] in rhyming_words:
            loc.append(i)
        else:
            pass
    return loc


def rep_loc(word, word_set):
    loc = []
    for i in range(len(word_set)):
        if word == word_set[i]:
            loc.append(i)
        else:
            pass
    return loc


def noun_loc(word_set):
    loc = []
    pos = nltk.pos_tag(word_set)
    rs = rhyme_scheme.split('_')
    if len(rs) > 2:
        if rs[2] == 'n':
            for i in range(len(word_set)):
                if pos[i][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                    loc.append(i)
                else:
                    pass
        elif rs[2] == 'v':
            for i in range(len(word_set)):
                if pos[i][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    loc.append(i)
                else:
                    pass
    else:
        for i in range(len(word_set)):
            if pos[i][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                loc.append(i)
            else:
                pass

    # diagnostic...
    #print pos
    #print loc
    # ...diagnostic

    return loc


def line_length_counter(b, word_list):
    lls = [b[0]]
    for i in range(1, len(b)):
        lls.append(b[i] - b[i-1])
    lls.append(len(word_list) - b[-1])
    return lls
    

def natural_breaks(sonnet):
    all_words = []
    for line in sonnet:
        all_words += line
    
    for i in range(len(all_words)):
        if ' ' in all_words[i]:
            spl = all_words[i].split(' ')
            all_words[i] = spl[0]
            for j in range(1, len(spl)):
                all_words.insert(i+j, spl[j])
        else:
            pass
    
    rhyme_locs = [rhyme_loc(w, all_words) for w in all_words]
    #slant_rhyme_locs = [slant_rhyme_loc(w, all_words) for w in all_words]
    noun_locs = noun_loc(all_words)
    
    breaks = []
    line_lengths = [len(all_words)]
    
    if any(bool(i) for i in rhyme_locs):
        for j in rhyme_locs:
            if bool(j):
                breaks += j
            else:
                pass
        breaks = sorted(list(set(breaks)))
        line_lengths = line_length_counter(breaks, all_words)
    else:
        pass
        
    #if max(line_lengths) <= len(all_words) / (len(sonnet) / 2):
    #    break
    #else:
    #    pass
    
    #if any(bool(i) for i in slant_rhyme_locs):
    #    for j in slant_rhyme_locs:
    #        if bool(j):
    #            breaks += j
    #        else:
    #            pass
    #    breaks = sorted(list(set(breaks)))
    #    line_lengths = line_length_counter(breaks, all_words)
    #else:
    #    pass
    #    
    #if max(line_lengths) <= len(all_words) / (len(sonnet) / 2):
    #    break
    #else:
    #    pass
    
    # maybe tweak this number...

    if len(breaks) <= (len(sonnet) / 2):
        breaks += noun_locs
    else:
        pass
    breaks = sorted(list(set(breaks)))
    
    #if breaks[-1] > len(all_words) - 4:
    #    breaks = breaks[:-1]
    #else:
    #    pass

    #breaks2 = []

    # diagnostic...
    #print breaks
    # ...diagnostic

    #for i in range(1, len(breaks)):
    #    if breaks[i] - breaks[i-1] >= 3:
    #        breaks2.append(breaks[i-1])
    #    else:
    #        pass

    # diagnostic...
    #print breaks
    #print breaks2
    #print all_words
    #print len(all_words)
    # ...diagnostic

    s = []
    s.append(all_words[:(breaks[0]+1)])
    for i in range(len(breaks)-1):
        s.append(all_words[breaks[i]+1:breaks[i+1]+1])
    s.append(all_words[breaks[-1]+1:len(all_words)+1])


    while len(s[-1]) > 0 and s[-1][-1] in banned_end_words:
        s[-1] = s[-1][:-1]
    if s[-1] == []:
        del s[-1]
    else:
        pass

    return s


def plagiarized(sonnet):
    for i in range(len(sonnet)-1):
        if any(sonnet[i] + sonnet[i+1] == vw[j:j+len(sonnet[i])+len(sonnet[i+1])] for j in xrange(len(vw) - len(sonnet[i]) - len(sonnet[i+1]) + 1)):
            plag = True
            break
        else:
            plag = False
    return plag


def banned_word_combo_fixer(l):
    l = ' '.join(l)
    for combo in banned_word_combos:
        if ' '.join(combo) in l:
            l = l.split(' ')
            for i in range(len(l) - len(combo)):
                if l[i:i+len(combo)] == combo:
                    l[i:i+len(combo)] = [random.choice(combo)]
                    l = ' '.join(l)
                    break
                else:
                    pass
        else:
            pass
    return l


if output_format.lower() == "pt":
    latex_lb = ""
elif output_format.lower() == "latex":
    latex_lb = "\\\\"
elif output_format.lower() == "read":
    latex_lb = "."

def sonnetizer():
    title = sw()
    s = generate_sonnet(title)
    while plagiarized(s):
        title = sw()
        s = generate_sonnet(title)
    s = plagiarism_syn_replace(s)
    
    # start of original plagarism checker...
    
    #s = plagiarism_check(s)
    #line_count = len(s)
    #while line_count < len(rhyme_scheme):
    #    s = generate_sonnet(sw())
    #    s = plagarism_checker(s)
    #    line_count = len(s)
    #s = s[:len(rhyme_scheme)]
    
    # ...end of original plagarism checker
    
    s = end_words(s)
    
    if "natural" in rhyme_scheme:
        s = natural_breaks(s)
    else:
        s = rhymer(s)
        while s[-1][-1] in banned_end_words:
            s[-1] = s[-1][:-1]
    sonnet = []
    for i in range(len(s)):
        line = s[i]
        line = banned_word_combo_fixer(line)
        line = line + latex_lb
        sonnet.append(line)
    return [' '.join(title).upper(), '\n'.join(sonnet) + '\n' + latex_lb + '\n' + latex_lb]

if show_diagnostics.lower() == 'y':
    print "assembling sonnets...\n\n"
for i in range(0,int(poem_count),2):
    sonnet1 = sonnetizer()
    sonnet2 = sonnetizer()
    if output_format == "latex":
        print '\\noindent'
    else:
        pass
    print str(i + 1) + '. ' + sonnet1[0] + latex_lb
    print sonnet1[1]
    print str(i + 2) + '. ' + sonnet2[0] + latex_lb
    print sonnet2[1]
    if output_format == "latex":
        print '\\newpage'
    else:
        pass