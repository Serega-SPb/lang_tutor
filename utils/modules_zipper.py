import os
import sys
import zipfile

input_dir = '../modules'
output_dir = '../_modules'


def create_zip(name, path):
    output_file = os.path.join(output_dir, f'{name}.zip')
    zip_arch = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
    path_lamb = lambda x: (x, x.split('\\', 1)[1])
    for rootdir, subdirs, files in os.walk(path):
        [zip_arch.write(*path_lamb(os.path.join(rootdir, f))) for f in files if not f.endswith('.pyc')]
    zip_arch.close()


def main():
    global input_dir, output_dir

    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[-1]

    print(f'Input folder: {input_dir}')
    print(f'Output folder: {output_dir}')

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for folder in os.listdir(input_dir):
        print(f'Creating {folder}.zip')
        create_zip(folder, os.path.join(input_dir, folder))
        print('='*25)
    print('Finished')


if __name__ == '__main__':
    main()

