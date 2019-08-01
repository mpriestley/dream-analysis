# created by Maria Priestley, priestleymaria@yahoo.co.uk

# Function to extract named entities from a text

from nltk import ne_chunk, pos_tag, word_tokenize, sent_tokenize

def get_named_entities(text):
    entities = []
    for sent in sent_tokenize(text):
       for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
          if hasattr(chunk, 'label'):
              ne = ' '.join(c[0] for c in chunk)
              if ne not in entities:
                  entities.append(ne)
    return entities