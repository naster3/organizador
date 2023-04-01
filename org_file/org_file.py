import os
from pathlib import Path
class formato:
    #diccionario de formato
    file_type={
        'IMAGENES':['.jpeg','.jpg','.tiff','.gif','.tmp','.png','.svg','.heif','.psd'],
        'AUDIO':['.aac','.aa','.dvf','.m4a','.m4b','.m4p','.mp3','.msv','.raw','.wav','.wma'],
        'VIDEOS': ['.avi', 'flv', '.wmv', '.mov', '.mp4', '.webm', '.vob', '.mng', '.qt', '.mpg', '.mpeg', '.3gp'],
        'DOCOUMENTS': ['.oxps', '.epub', '.pages', '.docx', '.doc', '.fdf', '.ods', '.odt', '.pwi', '.xsn', '.xps',
                    '.dotx', '.docm', '.dox', '.rvg', '.rtf', '.rtfd', '.wpd', '.xls', '.xlsx', '.ppt', '.pptx','.pdf'],
        'PROGRAMAN':['.py','.php','.js','.html','.css','.ps1','.exe','.zip']
    }

    #iteramos los formatos
    dct = dict()
    for directory, file_formats in file_type.items():
        for file_format in file_formats:
            dct[file_format] = directory


    def file_organizer():
        for entry in os.scandir():
            if entry.is_dir():
                continue

            file_path = Path(entry)
            file_format = file_path.suffix.lower()
            try:
                if file_format in formato.dct:
                    directory_path = Path(formato.dct[file_format])
                    directory_path.mkdir(exist_ok=True)
                    file_path.rename(directory_path.joinpath(file_path))

                else:
                    others = Path('OTHERS')
                    others.mkdir(exist_ok=True)
                    file_path.rename(others.joinpath(file_path))
            except FileExistsError:
                print(f'el archivo{file_path}ya existe')


if __name__ == '__main__':
    formato.file_organizer()
