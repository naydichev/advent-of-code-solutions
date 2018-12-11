#!/usr/bin/python

def main():
    fuel_cells = build_fuel_cells(serial=7315)

    find_max_power = search_fuel_cells(fuel_cells)

    print("Max fuel cell starts at coordinate", find_max_power)

def build_fuel_cells(serial):
    fuel_cells = [None]

    for x in range(1, 301):
        fuel_cells.append([None])
        for y in range(1, 301):
            rack_id = x + 10
            power = ((rack_id * y) + serial) * rack_id

            final_power = 0
            if power > 100:
                final_power = int(str(power)[-3])

            final_power -= 5
            fuel_cells[x].append(final_power)

    return fuel_cells

def search_fuel_cells(fuel_cells):
    max_coord = [None, None]
    max_total_power = 0

    for x in range(1, 298):
        for y in range(1, 298):
            grid_coords = [(i, j) for i in range(x, x + 3) for j in range(y, y + 3)]
            block_power = sum([fuel_cells[i][j] for i in range(x, x + 3) for j in range(y, y + 3)])
            if block_power > max_total_power:
                max_coord = [x, y]
                max_total_power = block_power

    return max_coord

if __name__ == "__main__":
    main()
