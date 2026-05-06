import matplotlib.pyplot as plt
from collections import defaultdict
import os
import time


class StatsSystem:
    def __init__(self):
        self.hourly_counts = defaultdict(lambda: {
            "car": 0,
            "delivery": 0,
            "bus": 0,
            "tram": 0
        })

        self.wait_times = []
        self.wait_times_by_type = defaultdict(list)

        self.approach_counts = defaultdict(int)

        self.time_bins = 24 * 6 
        self.flow_by_time = defaultdict(list)
        self.queue_by_time = defaultdict(list)

        self.simulation_finished = False

        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)

        self.run_id = int(time.time())

    def get_time_bin(self, sim):
        return int(sim.time_of_day * 6) % self.time_bins
    
    def update(self, sim, dt, index):
        t = self.get_time_bin(sim)

        spawn = next((s for s in sim.systems if hasattr(s, "spawned_total")), None)
        if spawn:
            time_h = sim.sim_time / 3600
            flow = spawn.spawned_total / max(0.001, time_h)
            self.flow_by_time[t].append(flow)

        total_queue = 0
        for lane in sim.intersection.lanes:
            light = lane.traffic_light

            for v in lane.vehicles:
                dx = light.x - v.x
                dy = light.y - v.y
                dist = (dx**2 + dy**2)**0.5

                if getattr(v, "is_stopped", False) and dist < 120:
                    total_queue += 1

        self.queue_by_time[t].append(total_queue)

        if sim.sim_time >= 24 * 3600 and not self.simulation_finished:
            self.simulation_finished = True
            self.generate_plots(sim)

    def register_vehicle(self, vehicle, sim):
        hour = int(sim.time_of_day)

        if hasattr(vehicle, "is_tram"):
            self.hourly_counts[hour]["tram"] += 1
        elif hasattr(vehicle, "is_bus"):
            self.hourly_counts[hour]["bus"] += 1
        elif hasattr(vehicle, "is_delivery"):
            self.hourly_counts[hour]["delivery"] += 1
        else:
            self.hourly_counts[hour]["car"] += 1

        if vehicle.lane and hasattr(vehicle.lane, "approach"):
            self.approach_counts[vehicle.lane.approach] += 1

    def register_wait_time(self, vehicle, wait_time):
        self.wait_times.append(wait_time)

        if hasattr(vehicle, "is_tram"):
            self.wait_times_by_type["tram"].append(wait_time)
        elif hasattr(vehicle, "is_bus"):
            self.wait_times_by_type["bus"].append(wait_time)
        elif hasattr(vehicle, "is_delivery"):
            self.wait_times_by_type["delivery"].append(wait_time)
        else:
            self.wait_times_by_type["car"].append(wait_time)

    def generate_plots(self, sim):
        print("=== GENERATING FULL STATS ===")

        hours = list(range(24))

        cars = [self.hourly_counts[h]["car"] for h in hours]
        buses = [self.hourly_counts[h]["bus"] for h in hours]
        trams = [self.hourly_counts[h]["tram"] for h in hours]
        delivery = [self.hourly_counts[h]["delivery"] for h in hours]

        time_labels = [i / 6 for i in range(self.time_bins)]

        avg_flow = [
            sum(self.flow_by_time[t]) / len(self.flow_by_time[t]) if self.flow_by_time[t] else 0
            for t in range(self.time_bins)
        ]

        avg_queue = [
            sum(self.queue_by_time[t]) / len(self.queue_by_time[t]) if self.queue_by_time[t] else 0
            for t in range(self.time_bins)
        ]

        plt.figure()
        plt.plot(hours, cars, label="car")
        plt.plot(hours, buses, label="bus")
        plt.plot(hours, trams, label="tram")
        plt.plot(hours, delivery, label="delivery")

        plt.xlabel("Godzina dnia")
        plt.ylabel("Liczba pojazdów")
        plt.title("Ruch godzinowy")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/hourly_{self.run_id}.png")
        plt.close()

        total = sum(cars)+sum(buses)+sum(trams)+sum(delivery)

        plt.figure()
        plt.pie([
            sum(cars)/total if total else 0,
            sum(buses)/total if total else 0,
            sum(trams)/total if total else 0,
            sum(delivery)/total if total else 0
        ], labels=["car","bus","tram","delivery"], autopct='%1.1f%%')

        plt.title("Struktura ruchu [%]")
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/structure_{self.run_id}.png")
        plt.close()

        plt.figure()
        plt.plot(time_labels, avg_flow)

        plt.xlabel("Godzina dnia")
        plt.ylabel("Pojazdy / godzina")
        plt.title("Natężenie ruchu")

        plt.xticks(range(0, 25, 2))
        plt.grid()

        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/flow_{self.run_id}.png")
        plt.close()

        plt.figure()
        plt.plot(time_labels, avg_queue)

        plt.xlabel("Godzina dnia")
        plt.ylabel("Średnia liczba pojazdów w korku")
        plt.title("Długość korka")

        plt.xticks(range(0, 25, 2))
        plt.grid()

        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/queue_{self.run_id}.png")
        plt.close()

        labels = []
        values = []

        for k, v in self.wait_times_by_type.items():
            if v:
                labels.append(k)
                values.append(sum(v)/len(v))

        plt.figure()
        plt.bar(labels, values)

        plt.xlabel("Typ pojazdu")
        plt.ylabel("Średni czas oczekiwania [s]")
        plt.title("Czas oczekiwania")
        plt.grid(axis='y')

        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/wait_by_type_{self.run_id}.png")
        plt.close()

        plt.figure()
        plt.bar(self.approach_counts.keys(), self.approach_counts.values())

        plt.xlabel("Wlot (A/B/C/D)")
        plt.ylabel("Liczba pojazdów")
        plt.title("Ruch per wlot")
        plt.grid(axis='y')

        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/approach_{self.run_id}.png")
        plt.close()

        avg_wait = sum(self.wait_times)/max(1,len(self.wait_times))

        with open(f"{self.results_dir}/stats_{self.run_id}.txt","w") as f:
            f.write("=== STATYSTYKI ===\n")
            f.write(f"Sredni czas oczekiwania: {avg_wait:.2f} s\n")
            f.write(f"Liczba pojazdow: {sum(cars)+sum(buses)+sum(trams)+sum(delivery)}\n")

        print("Zrobione. Wszystko w /results/")