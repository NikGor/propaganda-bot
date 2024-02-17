from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)


segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


def extract_nouns_and_propn(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    lemmatized_nouns_and_propn = []
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        if token.pos in {"NOUN", "PROPN"}:
            lemmatized_nouns_and_propn.append(token.lemma)

    return lemmatized_nouns_and_propn


def calculate_similarity(array1, array2):
    intersection = set(array1) & set(array2)
    num_matches = len(intersection)
    min_length = min(len(array1), len(array2))
    
    return num_matches / min_length if min_length > 0 else 0
