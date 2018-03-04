from collections import namedtuple

def read_jobs(path):
    jobs = list()
    with open(path, 'r') as handle:
        for line in handle.readlines()[1:]:
            info = line.split(' ')
            jobs.append(Job(int(info[0]), int(info[1])))
    return jobs


Job = namedtuple('Job', ('weight', 'length'))


def calculate_sum(jobs, scheduling_func):
    # Calculate scheduling score
    jobs_by_score = [(job, scheduling_func(job)) for job in jobs]
    # Sort by score then by weight
    sorted_jobs = sorted(jobs_by_score, key= lambda x: (x[1], x[0].weight),
                         reverse=True)
    # Calculate score
    total_sum = 0
    current_length = 0
    for (job, score) in sorted_jobs:
        current_length += job.length
        total_sum += current_length * job.weight
    return total_sum


def schedule_by_difference(job):
    return job.weight - job.length


def schedule_by_ratio(job):
    return job.weight/job.length
