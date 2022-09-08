import requests
from requests import Response
import logging
from tempfile import NamedTemporaryFile
from typing import Optional, List
import string
import random
from random import seed
from random import choice
import time

# from https://github.com/dwyl/english-words
DEFAULT_URL_EN_DICTIONARY: str = (
    "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
)


def count_line_fast(file_descriptor) -> int:
    """
    Get the number of line of a huge file fast
    from : https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    """

    def __make_gen(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    def raw_gen_count(file):
        f_gen = __make_gen(file.read)

        return sum(buf.count("\n") for buf in f_gen)

    return raw_gen_count(file_descriptor)


class GenerateEasy2RememberPassword:
    """
    Helps generating easy to remember Password from given dictionnary
    """

    # English words dic from https://github.com/dwyl/english-words
    DEFAULT_URL_EN_DICTIONARY: str = (
        "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    )

    def __init__(
        self,
        words: int = 2,
        min_length: int = 30,
        special_characters: int = 1,
        separator: str = "_",
        url_dict: Optional[str] = DEFAULT_URL_EN_DICTIONARY,
    ):
        """
        :param words: Num of words the pwd will contain
        :param min_length: Minimum length of the password to generate
        :param special_characters: Number of special characters included in the password
        :param url_dict: The URL to get the dictionary of words to generate the password,
        :param separator: Separator string betwin each words, default "_"
        default set to "DEFAULT_URL_DICTIONARY
        """
        self.words = words
        self.min_length = min_length
        self.special_characters = special_characters
        self.separator = separator
        self.url_dict = url_dict

    @staticmethod
    def get_random_list_of_int(
        max_num: int, length: int, extra_words: int = 0
    ) -> List[int]:
        """

        :param max_num: Max number of words to pick from
        :param length: Number of random number to return.
        :param extra_words: Number of extra random int you want
        :return:
        """
        # prepare a sequence
        sequence = [i for i in range(max_num)]
        result = [choice(sequence) for _ in range(length + extra_words)]
        result.sort()
        return result

    @staticmethod
    def get_random_special_characters(num: int) -> Optional[str]:
        if num > 0:
            random_str = "".join(
                [random.choice('!"#$%&\'()*+,-./:;<=>?@[]^`{|}~' + string.digits) for _ in range(num)]
            )
            logging.info(f"Random characters: {random_str}")
            return random_str
        raise ValueError(f"Invalid random characters number: {num}")

    @property
    def generate(self) -> str:
        """
        Download the dictionary in temporary directory, no persistence.
        Loop over the downloaded file line by line, not entirely bufferized to avoid stack overflow issues
        and memory overflow issues.
        :return: The generated pasword in string format
        """
        # Set Random seed on every call to guaranty the randomness of the random package
        seed(time.time())

        with NamedTemporaryFile(prefix="data_") as tempfile:
            # download the dictionary of words
            response: Response = requests.get(self.url_dict)

            if response.ok:
                tempfile.write(response.content)

                # Get the number of line of the dic file
                logging.info("Computing the number of line in the downloaded resource")
                with open(tempfile.name, "r") as dic_file:
                    max_words = count_line_fast(dic_file)
                    logging.info(f"lines: {max_words}")
                # Get random special characters
                special_character_list: Optional[str] = self.get_random_special_characters(
                    self.special_characters
                )
                logging.info(f"special_character_list: {special_character_list}")
                random_words: List[str] = []
                # generate the random list of integer to get the word from
                extra_words = (
                    0 if self.min_length <= 10 else 20
                )  # Add extra more slots in case it required huge min length password
                line_words = self.get_random_list_of_int(
                    max_words, self.words, extra_words=extra_words
                )
                logging.info(f"line_words: {line_words}")

                # Read the file and pick up random words from the dictionary of words
                index = 0
                line = 1
                current_pwd_size = self.special_characters
                with open(tempfile.name, "r") as file_descriptor:
                    for current_word in file_descriptor:
                        current_word: str = current_word.strip().lower().capitalize()
                        if len(random_words) >= self.words and current_pwd_size >= self.min_length:
                            logging.info("Fetch all words needed")
                            break
                        if line_words[index] == line:
                            random_words.append(current_word)
                            index += 1
                            current_pwd_size += len(current_word) + len(self.separator)
                        line += 1

                    # Shuffle the list to avoid redundancy on the beginning of the dictionary
                    random.shuffle(random_words)
                    # End the password with Special characters
                    random_words.append(special_character_list)

                generated_password = f"{self.separator}".join(random_words)
                return generated_password

