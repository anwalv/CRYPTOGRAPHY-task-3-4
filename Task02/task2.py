import hashlib, random, time, multiprocessing, struct

MESSAGE = b"give my friend 2 bitcoins for a pizza"
# тут я кілька разів запускала і по 8годин і більше з одним воркером, воно не в идавало резульат тому я радилась з ші 
# як првильно пришвидшити роботу, мені соромно що я сама не додумалась, але хотіла сказати що для пришвидшення я використала таку пораду від ші.
def worker(worker_id, found_flag, result_list):
    rng = random.Random()
    while not found_flag.value:
        prefix = struct.pack('>5I',
            rng.randint(0, 0xFFFFFFFF),
            rng.randint(0, 0xFFFFFFFF),
            rng.randint(0, 0xFFFFFFFF),
            rng.randint(0, 0xFFFFFFFF),
            rng.randint(0, 0xFFFFFFFF),
        )
        h = hashlib.sha256(prefix + MESSAGE).hexdigest()
        if h.startswith("00000000"):
            found_flag.value = 1
            result_list.append((prefix.hex(), h))
            return

if __name__ == "__main__":
    num_workers = multiprocessing.cpu_count()
    print(f"Ядер: {num_workers}. Старт!")

    found_flag = multiprocessing.Value('i', 0)
    manager = multiprocessing.Manager()
    result_list = manager.list()

    start = time.time()
    processes = [
        multiprocessing.Process(target=worker, args=(i, found_flag, result_list))
        for i in range(num_workers)
    ]
    for p in processes: p.start()
    for p in processes: p.join()

    elapsed = time.time() - start
    prefix_hex, h = result_list[0]
    print(f"Успіх за {elapsed:.1f}с!")
    print(f"Префікс (HEX): {prefix_hex}")
    print(f"Хеш: {h}")