#!/usr/bin/python

def main():
    fuel_cells = build_fuel_cells(serial=7315)

    find_max_power = search_fuel_cells(fuel_cells)

    print("Max fuel cell starts at coordinate", find_max_power)

def build_fuel_cells(serial):
    fuel_cells = []

    for x in range(300):
        fuel_cells.append([])
        for y in range(300):
            rack_id = (x + 1) + 10
            power = ((rack_id * (y + 1)) + serial) * rack_id

            final_power = 0
            if power > 100:
                final_power = int(str(power)[-3])

            final_power -= 5
            fuel_cells[x].append(final_power)

    return fuel_cells

def search_fuel_cells(fuel_cells):
    max_coord = [None, None]
    max_total_power = None
    square_size = None

    f_len = len(fuel_cells)
    for s in range(1, f_len + 1):
        for x in range(f_len - s + 1):
            for y in range(f_len - s + 1):
                block_power = sum([fuel_cells[i][j] for i in range(x, x + s) for j in range(y, y + s)])
                if block_power > max_total_power:
                    max_coord = [x + 1, y + 1]
                    max_total_power = block_power
                    square_size = s
        print("Size", s, "max coordinate", max_coord, "max power", max_total_power, "square at max power", square_size)

    print("\a")
    return max_coord, square_size

if __name__ == "__main__":
    main()
