all_calculations = ['NZD 10.0 is ILS 20.70', 'NZD 20.0 is ILS 41.40',
                    'NZD 30.0 is ILS 62.10', 'NZD 40.0 is ILS 82.80',
                    'NZD 50.0 is ILS 103.50', 'NZD 60.0 is ILS 124.20']

newest_first = list(reversed(all_calculations))

print("==== Oldest to Newest for File ====")
for item in all_calculations:
    print(item)

print()

print("==== Most Recent First ===")
for item in newest_first:
    print(item)
