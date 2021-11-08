"""
    PPM Image Editor

    Author: Kovit Virivong

    Date:   11-07-21

    This program contains various functions that can negate, greyscale, or remove red, green, or blue colors from
    an image. The main function asks the user for a modification to perform on a PPM file, and will output a copy
    of the image with the modification specified. It mainly relies on taking in lines of RGB values, converting
    them to lists, and then creating a new list with modifications to each element (RGB values). It then puts these
    modified lines of RGB values in a new PPM file.

"""
import math
import string


def process(lines, rows, cols):
    """
    process takes a list of strings and a dimension of rows and columns. It then merges the list into a single string,
    and then creates a new list of lists, where the amount of lists is the number of rows specified, and the number
    of pixels (R, G, and B values) is the number columns specified.

    :param lines: (list) list of strings
    :param rows: (int) number of sublists
    :param cols: (int) number of ints inside sublist
    :return: (list) list of lists containing ints
    """

    # converting list of strings to strings
    string_lines = ' '.join(lines)
    processed_lines = []
    # splitting string into elements in a list
    total_line = string_lines.split()
    for row in range(rows):
        rgb_line = []
        for i in range((cols * row) * 3, (cols * row + cols) * 3):
            rgb_line.append(int(total_line[i]))
        processed_lines.append(rgb_line)
    return processed_lines

def read_ppm(filename):
    """
    read_ppm is a function that opens a user specified file, finds the dimensions of the image in the heading, and
    converts the RGB values in the file to a list of strings, which it then sends to the process function in
    conjunction with the dimensions of the file.

    :param filename: (str) location of file and filename
    :return: (list) list of lists containing ints
    """

    with open(filename, "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()
        # splitting 2nd line of header to split dimensions
        cols = int(lines[1].split()[0])
        rows = int(lines[1].split()[1])
        return process(lines[3:], rows, cols)


def rgb_bound(rgb_value):
    """
    rgb_bound ensures that RGB values stay between 0 and 255.

    :param rgb_value: (int) RGB value
    :return: (int) changed RGB value if previous was > 255 or < 0, not changed otherwise
    """

    # upper bound
    if rgb_value > 255:
        rgb_value = 255
    # lower bound
    elif rgb_value < 0:
        rgb_value = 0
    return rgb_value


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

    rgb_line = line
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

    rgb_line = line
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

    rgb_line = [str(i) for i in line]
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
        rgb_line[i] = '0'
    rgb_line = ' '.join(rgb_line)
    return rgb_line


def brightness(line, bright_value):
    """
    brightness changes the brightness of each pixel by increasing or decreasing the RGB average value
    by user specifications.

    :param line: (str) string of RGB values
    :param bright_value: (int) brightness change percentage
    :return: (str) string of RGB values with changed brightness
    """
    rgb_line = line
    # initialize new list
    brightness_line = []
    # for loop going through every third element starting with the first
    for i in range(0, len(rgb_line), 3):
        # current pixel brightness calculated from set of RGB values
        current_brightness = (int(rgb_line[i]) + int(rgb_line[i + 1]) + int(rgb_line[i + 2])) / 3
        # pixel brightness multiplied by new brightness percentage added to each RGB value
        newbright_r = int(rgb_line[i]) + (current_brightness * (bright_value / 100))
        newbright_g = int(rgb_line[i + 1]) + (current_brightness * (bright_value / 100))
        newbright_b = int(rgb_line[i + 2]) + (current_brightness * (bright_value / 100))
        # R, G, B values (one set of RGB) with new brightness values added to new list
        brightness_line.extend([str(int(rgb_bound(newbright_r))), str(int(rgb_bound(newbright_g))),
                                str(int(rgb_bound(newbright_b)))])
    brightness_line = ' '.join(brightness_line)
    return brightness_line


def main():
    """
    The main function asks for an input and output filename. It will then ask for a desired modification through
    a list of numbers with corresponding modifications. If a valid number is entered, it will read the input file
    and start writing to it with the selected modification. It first writes the header information, and depending
    on the modification selected, it will run the corresponding function with each line of the body.

    """

    # input and output file name
    print("Your input file name should be your existing PPM file that you want to edit")
    in_filename = input("input file name:\n\t")
    print("Your output file name should not be an existing file, or else you risk overwriting it")
    out_filename = input("output file name:\n\t")
    extension = ".ppm"
    if extension not in out_filename.lower():
        print("Warning: your output file does not contain the .ppm extension")
        ext_input = input("Do you wish to add it?\nHit y for yes\nHit any key for no\n\t")
        if ext_input == "y":
            out_filename = out_filename.rstrip() + extension

    # lists modifications available
    print("Modifications available are:\n\t0. More info\n\t1. Invert color\n\t2. Convert to greyscale\n\t"
          "3. Remove red\n\t4. Remove green\n\t5. Remove blue\n\t6. Change brightness")
    valid_mods = "0123456"
    desired_mod = (input("enter the number of the desired modification\n\t"))
    bright_value = 0
    # while loop ensures that a number between 1 and 5 is inputted
    while desired_mod not in valid_mods or (len(desired_mod) != 1):
        print("please enter a valid number")
        desired_mod = (input("enter the number of the desired modification\n\t"))
    while desired_mod == "0":
        learn_mod = input("Enter the number of the modification you want to learn more about or hit any"
                          " key to continue modification:\n\t")
        while (learn_mod in "123456") and (learn_mod not in string.whitespace) and (len(learn_mod) == 1):
            if learn_mod == "1":
                print(
                    "\tInvert color will perform a color inversion on your image. Every color in the image\n\t"
                    "will be swapped to its complementary color, or its opposite image on the color wheel.\n\t"
                    "For example, red will turn green, and blue will turn orange. This can often help make\n\t"
                    "text easier to read.")
            elif learn_mod == "2":
                print(
                    "\tGreyscale conversion will convert your image to a greyscale image. All colors in the\n\t"
                    "the image will be converted to shades of grey. This is similar, but different to a \n\t"
                    "black and white image, where each pixel is either black or white.")
            elif learn_mod == "3":
                print(
                    "\tRemove red will remove all red colors from your image. This means that each pixel\n\t"
                    "will have its red value set to 0. Removing red colors will make your image appear \n\t"
                    "cyan tinted.")
            elif learn_mod == "4":
                print(
                    "\tRemove green will remove all green colors from your image. This means that each\n\t"
                    "pixel will have its green value set to 0. Removing green colors will make your image\n\t"
                    "appear magenta tinted.")
            elif learn_mod == "5":
                print(
                    "\tRemove blue will remove all blue colors from your image. This means that each pixel\n\t"
                    "will have its blue value set to 0. Removing blue colors will make your image appear \n\t"
                    "yellow tinted.")
            elif learn_mod == "6":
                print(
                    "Change brightness will change the brightness of your image. It does this by asking you what"
                    "percentage you want to change your brightness by and applies that percentage to each pixel."
                )
            learn_mod = input("Enter another number to learn more or hit enter to continue\n\t")
        desired_mod = (input("enter the number of the desired modification\n\t"))
        while desired_mod not in valid_mods or (len(desired_mod) != 1):
            print("please enter a valid number")
            desired_mod = (input("enter the number of the desired modification\n\t"))
    if desired_mod == "6":
        bright_value = input("What percentage brightness would you like to change it by?\n\t")
        while True:
            try:
                bright_value = int(bright_value)
                break
            except:
                print("Please enter a valid integer")
                bright_value = input("What percentage brightness would you like to change it by?\n\t")

    try:
        lines = read_ppm(in_filename)
    except IOError:
        print("problem opening file: " + in_filename)
    # variables assigned to input and output files
    with open(out_filename, "w", encoding="utf-8") as file_out:
        # header written out
        file_out.write("P3\n")
        # writing dimensions by counting length of pixels and number of rows
        file_out.write(str(len(lines[0]) // 3) + " " + str(len(lines)) + "\n")
        file_out.write("255\n")
        # body written to output file - for loop starts at 4th line and ends at last line
        for i in range(len(lines)):
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
            elif desired_mod == "6":
                file_out.write(brightness((lines[i]), int(bright_value)) + "\n")

    print("Image successfully modified")
    input("Press any key to exit")


if __name__ == '__main__':
    main()
