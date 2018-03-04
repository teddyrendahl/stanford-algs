############
# Standard #
############
import queue
import threading
import multiprocessing

############
# External #
############

###########
# Package #
###########


def table_from_file(path):
    """
    Create a dictionary from a file
    """
    with open(path, 'r') as f:
        return dict((int(i), None) for i in f.readlines())

def sum_is_possible(initial, total, table):
    """
    Find if the sum is in the table
    """
    required = total - initial
    return (required in table, required)


def find_all_two_sums(table, targets):
    """
    Find total number of two sum pairs for all given targets

    Parameters
    ----------
    table: dict

    targets: list
    """
    total = 0
    table_min = min(table.keys())
    table_max = max(table.keys())
    for target in targets:
        # Store used keys as to not double count
        for value in table:
            if (value + table_max >= target >= value + table_min):
                info = sum_is_possible(value, target, table)
                total += info[0]
    # Clear list of used values for next target
    print("Finished targets, found {} total combinations"
          "".format(total))
    return total/2


def threaded_find_two_sum(table, n=100):
    sums = multiprocessing.Queue()
    threads = list()
    # Launch all threads
    threaded_counter = lambda x, y: y.put(find_all_two_sums(table, x))
    partition = int(10000/n)
    for i in range(-n, n):
        print("Starting thread for {}".format((partition*i, partition*(i+1))))
        #th = threading.Thread(target=threaded_counter,
        #                      args=((list(range(partition*i, partition*(i+1))),)))
        th = multiprocessing.Process(target=threaded_counter,
                              args=((list(range(partition*i, partition*(i+1))),
                                     sums)))
        threads.append(th)
    for th in threads:
        th.start()
    # Wait for threads
    for th in threads:
        th.join()
    # Sum our response
    total = int(find_all_two_sums(table, [10000]))
    while not sums.empty():
        total += int(sums.get())
    return total
