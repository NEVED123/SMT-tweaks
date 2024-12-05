import verovio 
import os
import sys

tk = verovio.toolkit()

# from smt-plusplus
def toPNG(music_sequence, filename):
    tk.loadData(music_sequence)
    tk.setOptions({"pageWidth": 2100, "footer": 'none', 
                            'barLineWidth': 0.3, 'beamMaxSlope': 10, 
                            'staffLineWidth': 0.1, 'spacingStaff': 1})
    
    svg = tk.renderToSVG()

    with open(".temp.svg", 'w') as file:
        file.write(svg)

    os.system(f"inkscape -p .temp.svg -o {filename} -w 1000 --export-overwrite --export-type=png -b ffffff")
    os.remove(".temp.svg")

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as file:
        sequence = ''.join(file.readlines())

    print(sequence)

    toPNG(sequence, output_file)