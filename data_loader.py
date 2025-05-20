import string

def load_dictionary(file_path):
    phrase_to_id = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            phrase, phrase_id = line.strip().split('|')
            phrase_to_id[phrase] = int(phrase_id)
    return phrase_to_id

def load_sentiment_labels(file_path):
    phrase_id_to_sentiment = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # skip header if present
        for line in f:
            phrase_id, sentiment_score = line.strip().split('|')
            phrase_id_to_sentiment[int(phrase_id)] = float(sentiment_score)
    return phrase_id_to_sentiment

def load_sentences(file_path):
    sentences = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            idx, sentence = line.strip().split('\t')
            sentences[int(idx)] = sentence
    return sentences

def load_splits(file_path):
    splits = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            idx, split_label = line.strip().split(',')
            splits[int(idx)] = int(split_label)  # 1=train, 2=dev, 3=test
    return splits

def preprocess_text(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

def build_dataset(dictionary_path, sentiment_path, sentences_path, splits_path):
    phrase_to_id = load_dictionary(dictionary_path)
    phrase_id_to_sentiment = load_sentiment_labels(sentiment_path)
    sentences = load_sentences(sentences_path)
    splits = load_splits(splits_path)

    train_data = []
    dev_data = []
    test_data = []

    for idx, sentence in sentences.items():
        proc_sentence = preprocess_text(sentence)
        phrase_id = phrase_to_id.get(proc_sentence)
        if phrase_id is None:
            continue
        sentiment_score = phrase_id_to_sentiment.get(phrase_id)
        if sentiment_score is None:
            continue
        split = splits.get(idx)
        if split == 1:
            train_data.append((sentence, sentiment_score))
        elif split == 2:
            dev_data.append((sentence, sentiment_score))
        elif split == 3:
            test_data.append((sentence, sentiment_score))

    return train_data, dev_data, test_data
