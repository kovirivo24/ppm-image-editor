"""
    CS051P Lab Assignments: Lab06 - Image Processing 1

    Author: Kovit Virivong

    Date:   10-28-21

    This program contains various functions that can negate, greyscale, or remove red, green, or blue colors from
    an image. The main function asks the user for a modification to perform on a PPM file, and will output a copy
    of the image with the modification specified. It mainly relies on taking in lines of RGB values, converting
    them to lists, and then creating a new list with modifications to each element (RGB values). It then puts these
    modified lines of RGB values in a new PPM file.

"""
import math


def decode(in_filename, out_filename):
    """
    decode takes in a PPM file and decodes its RGB values and writes it into a new PPM file. This will output a decoded
    image, and if it was a specific starting image, then the new image will contain a statement.

    :param in_filename: (str) existing PPM file
    :param out_filename: (str) new PPM file with coded RGB values
    :return: None
    """

    with open(in_filename, "r", encoding="utf-8") as file_in, open(out_filename, "w", encoding="utf-8") as file_out:
        lines = file_in.readlines()
        # prints header
        for i in range(3):
            file_out.write(lines[i])
        # prints body (starting from 4th line down length of file)
        for i in range(3, len(lines)):
            # initialize a new list
            single_line = []
            line_list = lines[i].split()
            for j in range(len(line_list)):
                if int(line_list[j]) % 3 == 0:
                    line_list[j] = "0"
                elif int(line_list[j]) % 3 == 1:
                    line_list[j] = "153"
                elif int(line_list[j]) % 3 == 2:
                    line_list[j] = "255"
                # extend each list by a new string containing new number
                single_line.append(str(line_list[j]))
            # convert list into a string
            file_out.write(' '.join(single_line) + "\n")


def main_part1():
    """
    This main_part1 calls the decode function with the image part1.ppm. part1.ppm has its RGB values set up so that
    decode will change its rgb values specifically so that it will display a certain image.
    """

    decode("files/part1.ppm", "main1_part1.ppm")


def negate(line):
    """
    negate takes in a string of RGB values and negates it, or in other words subtracts each RGB value from 255.
    Thus, the RGB value is inverted.

    :param line: (str) string of RGB values
    :return: (str) string of negated RGB values
    """

    rgb_line = line.split()
    # initialize new list
    negated_line = []
    # for loop going through each element (RGB value) in list
    for i in range(len(rgb_line)):
        # extending list by negated RGB value
        negated_line.extend([str(255 - int(rgb_line[i]))])
    negated_line = ' '.join(negated_line)
    return negated_line


def grey_scale(line):
    """
    grey_scale takes in a string of RGB values and turns them into grey values. Grey values are the square root of
    the sum of squared RGB values. grey_scale does this operation on every set of three RGB values, and replaces
    all of them with the same grey value.

    :param line: (str) string of RGB values
    :return: (str) string of grey values
    """

    rgb_line = line.split()
    # initialize new list
    greyscale_line = []
    # for loop going through every third element starting with the first
    for i in range(0, len(rgb_line), 3):
        # grey value calculated from set of RGB values
        grey_value = math.sqrt(int(rgb_line[i]) ** 2 + int(rgb_line[i + 1]) ** 2 + int(rgb_line[i + 2]) ** 2)
        # ensures that grey value does not exceed 255
        if grey_value > 255:
            grey_value = 255
        # R, G, B values (one set of RGB) being extended with the same grey value
        greyscale_line.extend([str(int(grey_value))] * 3)
    greyscale_line = ' '.join(greyscale_line)
    return greyscale_line


def remove_color(line, color):
    """
    remove_color removes a color from every set of RGB values depending on the parameter color. It simply sets the
    corresponding color value (R, G, or B) to 0. Removing red should make the image appear cyan tinted, removing green
    should make the image appear magenta tinted , and removing blue should make the image appear yellow tinted.

    :param line: (str) string of RGB values
    :param color: (str) color to remove
    :return: (str) string of RGB values with removed color
    """

    rgb_line = line.split()
    # create a copy of rgb_line
    removed_line = list(rgb_line)
    # initialize variable
    clr = None
    # sets starting point for for loop depending on color
    if color == "red":
        clr = 0
    elif color == "green":
        clr = 1
    elif color == "blue":
        clr = 2
    # sets R,G, or B to 0
    for i in range(clr, len(rgb_line), 3):
        removed_line[i] = '0'
    removed_line = ' '.join(removed_line)
    return removed_line


def main():
    """
    The main function asks for an input and output filename. It will then ask for a desired modification through
    a list of numbers with corresponding modifications. If a valid number is entered, it will read the input file
    and start writing to it with the selected modification. It first writes the header information, and depending
    on the modification selected, it will run the corresponding function with each line of the body.

    """

    # input and output file name
    in_filename = input("input file name:\n\t")
    out_filename = input("output file name:\n\t")

    # lists modifications available
    print("modifications are:\n\t1. negate\n\t2. greyscale\n\t3. remove red\n\t4. remove green\n\t5. remove blue")
    valid_mods = "123456"
    desired_mod = (input("enter the number of the desired modification\n\t"))
    # while loop ensures that a number between 1 and 5 is inputted
    while desired_mod not in valid_mods or (len(desired_mod) != 1):
        print("please enter a valid number")
        desired_mod = (input("enter the number of the desired modification\n\t"))

    # variables assigned to input and output files
    with open(in_filename, "r", encoding="utf-8") as file_in, open(out_filename, "w", encoding="utf-8") as file_out:
        # lines in input file read
        lines = file_in.readlines()
        # header written to output file
        for i in range(3):
            file_out.write(lines[i])
        # body written to output file - for loop starts at 4th line and ends at last line
        for i in range(3, len(lines)):
            # if statements change which function is used depending on modification selected
            if desired_mod == "1":
                file_out.write(negate(lines[i]) + "\n")
            elif desired_mod == "2":
                file_out.write(grey_scale(lines[i]) + "\n")
            elif desired_mod == "3":
                file_out.write(remove_color((lines[i]), "red") + "\n")
            elif desired_mod == "4":
                file_out.write(remove_color((lines[i]), "green") + "\n")
            elif desired_mod == "5":
                file_out.write(remove_color((lines[i]), "blue") + "\n")


if __name__ == '__main__':
    # main_part1()  # comment this out after you check-in for part 1
    main()  # uncomment this after you check-in for part 1
