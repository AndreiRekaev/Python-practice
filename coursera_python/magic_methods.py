import os.path
import uuid
import tempfile




class File:

    def __init__(self, path_to_file):
        self.path = path_to_file
        if not os.path.isfile(self.path):
            open(self.path, 'tw', encoding='utf-8')
            self.text = ''
        else:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.count = f.readlines()
                self.text = ''
                for line in self.count:
                    self.text += line
                self.end = len(self.count)
            f.closed
        self.current = 0

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.count = f.readlines()

            self.text = ''
            for line in self.count:
                self.text += line
            self.end = len(self.count)
            return(self.text)
        f.closed

    def write(self, text):
        with open(self.path, 'w') as f:
            self.text = text
            f.write(self.text)
            self.count = self.text.split('\n')
            self.end = len(self.count)
        f.closed

    def __add__(self, file_obj):
        if isinstance(file_obj, File):
            new_text = self.text + file_obj.text
        else:
            new_text = ''

        new_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        new_file = File(new_path)
        new_file.text = new_text
        new_file.write(new_text)
        return (new_file)

    def __str__(self):
        return self.path

    def __iter__(self):
        self.temp = self.current
        return self

    def __next__(self):
        if self.temp >= self.end:
            raise StopIteration
        result = self.count[self.temp]
        self.temp += 1
        if result != "":
            return result
        else:
            raise StopIteration



Отладка:
>>> import os.path
>>> from solution import File
>>> path_to_file = 'some_filename'
>>> os.path.exists(path_to_file)
False
>>> file_obj = File(path_to_file)
>>> os.path.exists(path_to_file)
True
>>> print(file_obj)
some_filename
>>> file_obj.read()
''
>>> file_obj.write('some text')
9
>>> file_obj.read()
'some text'
>>> file_obj.write('other text')
10
>>> file_obj.read()
'other text'
>>> file_obj_1 = File(path_to_file + '_1')
>>> file_obj_2 = File(path_to_file + '_2')
>>> file_obj_1.write('line 1\n')
7
>>> file_obj_2.write('line 2\n')
7
>>> new_file_obj = file_obj_1 + file_obj_2
>>> isinstance(new_file_obj, File)
True
>>> print(new_file_obj)
C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
>>> for line in new_file_obj:
....    print(ascii(line))  
'line 1\n'
'line 2\n'
>>> new_path_to_file = str(new_file_obj)
>>> os.path.exists(new_path_to_file)
True
>>> file_obj_3 = File(new_path_to_file)
>>> print(file_obj_3)
C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
>>>
