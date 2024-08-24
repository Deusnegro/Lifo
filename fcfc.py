import matplotlib.pyplot as plt


def draw_gantt_chart(timeline, title, filename="gantt_chart.png"):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')

    yticks = []
    ylabels = []
    for i, (start, finish, name) in enumerate(timeline):
        gnt.broken_barh([(start, finish - start)], (i * 10, 9), facecolors=('tab:blue'))
        yticks.append(i * 10 + 4.5)
        ylabels.append(name)

        # Add a tag with the process name and start time
        gnt.text((start + finish) / 2, i * 10 + 4.5, f'{name} ({start}-{finish})', 
                 ha='center', va='center', color='white', fontsize=10, weight='bold')

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(ylabels)
    gnt.grid(True)
    plt.title(title)
    plt.savefig(filename)
    print(f"Gantt chart saved as {filename}")

def fcfs(processes):
    print(processes)
    
    processes.sort(key=lambda x: x['arrival'])
    print(processes)
    current_time = 0
    timeline = []

    for process in processes:
        print(f"this is my prosess  {process}")
        if current_time < process['arrival']:
            current_time = process['arrival']
        
        
        process['start'] = current_time
        current_time += process['burst']
        process['finish'] = current_time
        timeline.append((process['start'], process['finish'], process['name']))

    draw_gantt_chart(timeline, "FCFS Scheduling", filename="fcfs_gantt_chart.png")

def sjf(processes):
    processes.sort(key=lambda x: (x['arrival'], x['burst']))
    current_time = 0
    timeline = []

    for process in processes:
        if current_time < process['arrival']:
            current_time = process['arrival']
        process['start'] = current_time
        current_time += process['burst']
        process['finish'] = current_time
        timeline.append((process['start'], process['finish'], process['name']))

    draw_gantt_chart(timeline, "SJF Scheduling", filename="sjf_gantt_chart.png")

def rr(processes, quantum):
    queue = []
    timeline = []
    current_time = 0

    for process in processes:
        queue.append(process.copy())

    while queue:
        process = queue.pop(0)
        if current_time < process['arrival']:
            current_time = process['arrival']
        if process['burst'] > quantum:
            start = current_time
            current_time += quantum
            finish = current_time
            process['burst'] -= quantum
            queue.append(process)
        else:
            start = current_time
            current_time += process['burst']
            finish = current_time

        timeline.append((start, finish, process['name']))

    draw_gantt_chart(timeline, "Round Robin Scheduling", filename="rr_gantt_chart.png")

def srtf(processes):
    timeline = []
    current_time = 0
    remaining_processes = processes.copy()

    while remaining_processes:
        # Filter processes that have arrived by the current time and are not finished
        arrived_processes = [p for p in remaining_processes if p['arrival'] <= current_time]
        if arrived_processes:
            # Select the process with the shortest remaining burst time
            current_process = min(arrived_processes, key=lambda x: x['burst'])
            start = current_time
            finish = current_time + 1
            current_time = finish
            current_process['burst'] -= 1
            timeline.append((start, finish, current_process['name']))
            if current_process['burst'] == 0:
                remaining_processes.remove(current_process)
        else:
            current_time += 1

    draw_gantt_chart(timeline, "SRTF Scheduling", filename="srtf_gantt_chart.png")

if __name__ == "__main__":
    processes = [
        {'name': 'P1', 'arrival': 0, 'burst': 3},
        {'name': 'P2', 'arrival': 1, 'burst': 5},
        {'name': 'P3', 'arrival': 2, 'burst': 7},
        {'name': 'P4', 'arrival': 3, 'burst': 8}
    ]

    # Run all algorithms and generate Gantt charts
    fcfs(processes)
    sjf(processes)
    rr(processes, quantum=3)
    srtf(processes)

