#!/usr/bin/env python3

import os
import random
import string
import nltk

nltk.download('words')
from nltk.corpus import words

word_list = words.words()


def create_random_word():
  return ''.join(random.choices(word_list, k=random.randint(1, 3))).lower()


def create_dir_structure(depth, max_dirs, extensions):
  """
    Creates a directory structure with random-ish names and files at each level.

    Args:
    depth (int): The depth of the directory structure.
    max_dirs (int): The maximum number of directories at each level.
    extensions (list): List of file extensions to be used.

    Returns:
    None
    """
  if depth <= 0:
    return
  num_dirs = random.randint(1, max_dirs)
  for _ in range(num_dirs):
    dir_name = create_random_word()
    os.makedirs(dir_name)
    num_files = random.randint(1, 5)
    for _ in range(num_files):
      file_name = create_random_word() + random.choice(extensions)
      open(os.path.join(dir_name, file_name), 'a').close()
    create_dir_structure(depth - 1, max_dirs, extensions)


create_dir_structure(3, 4, ['.txt', '.doc', '.mp4'])
