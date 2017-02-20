import os
import shutil
import zipfile

DATA_IMPORT_PATH= 'data/'
DATA_EXPORT_PATH = 'docs/data/'
PAGES = [
    { 'name': 'portraits', 'import': 'data/portraits/', 'export': 'docs/portraits/' },
    { 'name': 'faces', 'import': 'data/faces/', 'export': 'docs/faces/' },
]


def remake_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    
    os.mkdir(path)


remake_dir(DATA_EXPORT_PATH)

for dirname in os.listdir(DATA_IMPORT_PATH):
    zip = zipfile.ZipFile(DATA_EXPORT_PATH + dirname + '.zip', 'w')
    for index, filename in enumerate(os.listdir(DATA_IMPORT_PATH + dirname)):
        root, ext = os.path.splitext(filename)
        
        load_path = DATA_IMPORT_PATH + dirname + '/' + filename
        save_path = '%03d' % (index + 1) + ext

        zip.write(load_path, save_path)

    zip.close()


for page in PAGES:
    remake_dir(page['export'])

    template = ''

    for index, filename in enumerate(os.listdir(page['import'])):
        root, ext = os.path.splitext(filename)

        save_name = ('%03d' % (index + 1)) + ext
        shutil.copyfile(page['import'] + filename, page['export'] + save_name)
        
        src = page['name'] + '/' + save_name
        template += '<div><a href="' + src + '" data-lightbox="image" alt="' + save_name + '">'
        template += '<img style="border: thin solid #333333" src="' + src + '"></a></div>\n'

    f = open('template.html', encoding='utf-8')
    html = f.read()
    f.close()

    html = html.replace('<!-- SLICK -->', template)
    html = html.replace('<!-- NAME -->', page['name'])

    f = open('docs/' + page['name'] + '.html', 'w', encoding='utf-8')
    f.write(html)
    f.close()
