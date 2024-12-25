import argparse
import csv
import struct

MEMORY_SIZE = 1024


def parse_args():
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")
    parser.add_argument("mode", choices=["assemble", "interpret"], help="Operation mode")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("--output_file", help="Output file")
    parser.add_argument("--log_file", help="Log file (CSV format)")
    parser.add_argument("--result_file", help="Result file for interpreter (CSV format)")
    parser.add_argument("--memory_range", help="Memory range for interpreter (start:end)")
    return parser.parse_args()


def assemble_instruction(instruction):
    a = instruction["A"] & 0x7F  # 7 бит
    b = instruction["B"] & 0xFFFFFFFF  # 32 бита
    # Собираем 5 байт
    byte1 = a
    byte2, byte3, byte4, byte5 = struct.unpack("4B", struct.pack("<I", b))
    return [byte1, byte2, byte3, byte4, byte5]


def assemble(input_file, output_file, log_file):
    instructions = []
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            a, b = map(int, line.split(","))
            instructions.append({"A": a, "B": b})

    binary_data = []
    with open(log_file, "w", newline="") as log_csv:
        csv_writer = csv.writer(log_csv)
        csv_writer.writerow(["A", "B", "Bytes"])
        for instruction in instructions:
            bytes_list = assemble_instruction(instruction)
            binary_data.extend(bytes_list)
            csv_writer.writerow([instruction["A"], instruction["B"], bytes_list])

    with open(output_file, "wb") as bin_file:
        bin_file.write(bytearray(binary_data))


def interpret(input_file, result_file, memory_range):
    memory = [0] * MEMORY_SIZE
    accumulator = 0

    # Читаем бинарный файл
    try:
        with open(input_file, "rb") as f:
            binary_data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Интерпретация команд
    for i in range(0, len(binary_data), 5):
        if i + 5 > len(binary_data):
            break
        command = binary_data[i:i + 5]
        a = command[0]  # Код команды
        b = struct.unpack("<I", command[1:])[0]  # Операнд

        if a == 120:  # Загрузка константы
            accumulator = b
        elif a == 101:  # Чтение из памяти
            accumulator = memory[b]
        elif a == 36:  # Запись в память
            memory[b] = accumulator
        elif a == 51:  # Операция "!="
            memory[b] = int(memory[b] != accumulator)

    # Диапазон памяти
    try:
        start, end = map(int, memory_range.split(":"))
        if not (0 <= start <= end < MEMORY_SIZE):
            raise ValueError("Invalid memory range.")
    except ValueError:
        print("Error: Invalid memory range. Use 'start:end', where 0 <= start <= end < MEMORY_SIZE.")
        return

    # Сохраняем результат
    with open(result_file, "w", newline="") as result_csv:
        csv_writer = csv.writer(result_csv)
        csv_writer.writerow(["Address", "Value"])
        for addr in range(start, end + 1):
            csv_writer.writerow([addr, memory[addr]])


def main():
    args = parse_args()
    if args.mode == "assemble":
        if not args.output_file or not args.log_file:
            print("Error: --output_file and --log_file are required for assembling.")
            return
        assemble(args.input_file, args.output_file, args.log_file)
    elif args.mode == "interpret":
        if not args.result_file or not args.memory_range:
            print("Error: --result_file and --memory_range are required for interpretation.")
            return
        interpret(args.input_file, args.result_file, args.memory_range)


if __name__ == "__main__":
    main()


#python main.py assemble file.txt --output_file output.bin --log_file log.csv
#python main.py interpret output.bin --result_file result.csv --memory_range 0:10

