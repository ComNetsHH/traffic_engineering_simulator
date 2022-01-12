import matplotlib.pyplot as plt
import numpy as np
import os

class Stats(object):
    experiment_name='main'
    def set_experiment_name(name):
        os.makedirs(f'./results/{name}', exist_ok=True)
        Stats.experiment_name = name

    def evaluate(data_centers, verbose=False):
        total_received = 0
        total_dropped = 0
        delays = []
        for d in data_centers:
            if verbose:
                print(f'DataCenter<{d.id}>')
                print(f'  Requests Received: {d.num_received}')
                print(f'  Requests Processed: {d.num_processed}')
                print(f'  Requests Dropped: {d.num_dropped}')
                print(f'  Utilization: {(d.get_utilization()*100):.2f}%')
                print(f'  Avg Requests in the System: {d.get_average_requests_in_system():.2f}')
                print(f'  Avg Requests in the Queue: {d.get_average_queue_length():.2f}')
                print(f'  Avg Delay: {np.mean(d.get_delays()):.2f}s')
                print('')
            Stats.plot_ts([x['time'] for x in d.ts], [x['in_service'] + x['queued'] for x in d.ts], 'Number of Requests in the Data Center', 'Time [s]', 'Number of Requests', f'requests_ts_{d.id}')
            Stats.plot_histogram(d.get_delays(), 'Delay Distribution', 'Delay [s]', 'Probability', f'delay_dist_{d.id}')

            total_received += d.num_received
            total_dropped += d.num_dropped
            delays += d.get_delays()
        print(f'---- Summary ----')
        print(f'Total Blocking Probability: {100* total_dropped/total_received:.2f}%')
        print(f'Average Delay: {np.mean(delays):.2f}s')


    def plot_ts(t, v, title='', x_label = '', y_label='', fname='ts'):
        fig = plt.figure()
        plt.plot(t,v)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        fig.tight_layout()
        fig.savefig(f"./results/{Stats.experiment_name}/{fname}.png", dpi=500, bbox_inches='tight', pad_inches=0.01)
        plt.close()

    def plot_histogram(v, title='', x_label = '', y_label='', fname='hist'):
        fig = plt.figure()
        plt.hist(v, density=True, edgecolor='#fff')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        fig.tight_layout()
        fig.savefig(f"./results/{Stats.experiment_name}/{fname}.png", dpi=500, bbox_inches='tight', pad_inches=0.01)
        plt.close()