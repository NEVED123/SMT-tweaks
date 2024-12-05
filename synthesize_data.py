import numpy as np
from krn2png import toPNG
import cv2

def generate_kern_time_signature():
    numerator = np.random.choice([2,3,4,6,8,12])
    denominator = np.power(2, np.random.choice([1,2,3,4]))
    return f"*M{numerator}/{denominator}", numerator, denominator

def generate_kern_key_signature():
    keys = ['f#c#g#d#a#e#b#', 'b-e-a-d-g-c-f-']
    i = (np.random.randint(0, 7) * 2) + 1
    return f'*k[{np.random.choice(keys)[:i + 1]}]'

def generate_kern_measure(measure_num, numerator, denominator):

    if not float(np.log2(denominator)).is_integer():
        raise Exception(f"denominator {denominator} is not a power of 2!")
    
    if measure_num == 1:
        barline = f'={measure_num}-\t={measure_num}-\n'
    else:
        barline = f'={measure_num}\t={measure_num}\n'

    # need to come up with a subdivision of this measure
    total_subdivisions = numerator * 4
    treble_staff = []
    bass_staff = []
    for staff in [treble_staff, bass_staff]:
        subdivisions = []
        sumdivisions = sum(subdivisions)
        while sumdivisions < total_subdivisions:
            remaining = total_subdivisions - sumdivisions
            subdivisions.append(np.random.randint(1, remaining + 1))
            sumdivisions = sum(subdivisions)

        subdivision_types = [(i, np.random.choice([0,1])) for i in subdivisions]
        largest_frac_of_whole_note = denominator * 4 
    
        kern_subdivisions = ['.' for _ in range(total_subdivisions)]
        placement = 0
        for subdivision in subdivision_types:
            e = largest_frac_of_whole_note #largest frac should always be a power of 2
            while e > 0:
                partial_length = subdivision[0] & e
                if partial_length > 0:
                    type = 'r' if subdivision[1] == 0 else np.random.choice(['a','b','c','d','e','f','g'])
                    note_value = largest_frac_of_whole_note // partial_length
                    kern_subdivisions[placement] = f'{note_value}{type}'
                    placement += partial_length
                e //= 2

        staff.extend(kern_subdivisions)

    treble_staff_clean = []
    bass_staff_clean = []
    for i in range(total_subdivisions):
        if not treble_staff[i] == bass_staff[i] == '.':
            treble_staff_clean.append(treble_staff[i])
            bass_staff_clean.append(bass_staff[i])

    kern_measure = ''
    for i in range(len(treble_staff_clean)):
        kern_measure += f'{bass_staff_clean[i]}\t{treble_staff_clean[i]}\n'

    return barline + kern_measure
    

def generate_full_kern():
    kern_header = '**kern\t**kern\n'
    staff_header = '*staff2\t*staff1\n'
    clefs = '*clefF4\t*clefG2\n'
    time_signature, numerator, denominator = generate_kern_time_signature()
    staff_time_signatures = f'{time_signature}\t{time_signature}\n'
    key_signature = generate_kern_key_signature()
    staff_key_signatures = f'{key_signature}\t{key_signature}\n'
    
    full_kern = kern_header + staff_header + clefs + staff_key_signatures + staff_time_signatures

    # for i in range(1, np.random.randint(33)):
    for i in range(5):
        full_kern += generate_kern_measure(i+1, numerator, denominator)

    full_kern += '*-\t*-'

    return full_kern

def deform_image(filename, mean=0, std=25):
    image = cv2.imread(filename)

    noise = np.random.normal(mean, std, image.shape).astype(np.float32)
    noisy_image = image.astype(np.float32) + noise
    image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    height, width = image.shape[:2]

    max_skew_factor = 0.05

    skewx = np.random.uniform(-max_skew_factor,max_skew_factor)
    skewy = np.random.uniform(-max_skew_factor,max_skew_factor)

    skew_matrix = np.float32([
        [1, skewx, 0],
        [skewy, 1, 0]
    ])

    skewed_image = cv2.warpAffine(image, skew_matrix, (width, height))
    cv2.imwrite(filename, skewed_image)

if __name__ == "__main__":
    kern = generate_full_kern()

    with open('mykern.krn', 'w') as file:
        file.write(kern)

    filename = "output.png"
    toPNG(kern, filename)
    deform_image(filename)