"""
Password Generator that creates 20k approx passwords with 8 to 12 characters
Designed for eduction and CTFs. Passwords should not be considered secure and
should NOT be used in a production environment or at home.
written by hand originally, modified with some suggestions from chat gpt, which broke the code
then fixed by hand, now tyring to make it fast...
helpful: https://www.youtube.com/watch?v=BZzb_Wpag_M - cProfile
"""
import multiprocessing
from random import choice
import string
import os
from time import time


start_time = time()

CHARACTER_SET = string.digits + string.ascii_letters + string.punctuation
PASSWORD_LENGTHS = range(8, 12)
MAX_PASSWORDS = 20000
TOTAL_PROCESSES = 3
CHUNK = 500
# use constants here so code can quickly be updated as needed


def generate_password(length):
    return ''.join(choice(CHARACTER_SET) for _ in range(length))
    # return a string made of a random set of 8 to 12 chars


def generate_variations(password):
    variations = [
        password,
        password.swapcase(),
        password.upper(),
        password.lower()
    ]
    return variations

# for i in range(10):
#     i = generate_password(12)
#     print(i)


def generate_passwords(worker_id, working_lock, working_word_set, working_word_list):
    chunk_size = CHUNK
    while len(working_word_list) < MAX_PASSWORDS:
        password_chunk = [generate_password(choice(PASSWORD_LENGTHS)) for _ in range(chunk_size)]
        #password_length = choice(PASSWORD_LENGTHS)
        #new_password = generate_password(password_length)

        with working_lock:
            for new_password in password_chunk:
                if new_password not in working_word_set:
                    working_word_set.add(new_password)
                    working_word_list.extend(generate_variations(new_password))

    print(f"Worker {worker_id} finished generating passwords.")


def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item}\n")


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    word_list = manager.list()
    lock = multiprocessing.Lock()
    word_set = set()
    processes = []
    for i in range(TOTAL_PROCESSES):
        n = i
        process = multiprocessing.Process(target=generate_passwords, args=(n, lock, word_set, word_list))
        process.start()
        processes.append(process)
        # print('module name:', __name__)
        # print('parent process:', os.getppid())
        # print('process id:', os.getpid())

    for process in processes:
        process.join()

    # timing stats
    print("All workers finished generating passwords.")
    end_time = time()
    print(f'Program took {(end_time - start_time):.2f} seconds with {TOTAL_PROCESSES} processes.')

    # adjusting the output to create files each tim it runs
    file_title = input('What do you want to call your password_list?')
    output_file = 'passwords_' + file_title + '.txt'
    save_to_file(output_file, word_list)
    print(f"Results saved to {output_file}")

