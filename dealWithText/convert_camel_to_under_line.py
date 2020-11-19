import json
import os
import re
import numbers
import sys

'''将驼峰格式的json转换为大写+下划线格式的json,直接在python命令行中运行'''


class ConvertCamel:
    @staticmethod
    def convert_key(line_content: str) -> str:
        line_content = line_content[0].upper() + line_content[1:]
        split_contents = re.findall('[A-Z][^A-Z]*', line_content)
        new_contents = list()
        for value in split_contents:
            new_contents.append(value.upper())
        return '_'.join(new_contents)

    @staticmethod
    def cover_camel(path):
        (file, ext) = os.path.splitext(path)
        (dir_path, file_name) = os.path.split(path)
        # 下划线文件的路径
        under_line_file_path = dir_path + file_name + '_userLine'
        new_dict = dict()
        # 读取json文件
        with open(path) as fd:
            content = json.load(fd)
        # 解析json文件中的key，将驼峰转换为大写加下划线的字符串
        for key, value in content.items():
            new_key = ConvertCamel.convert_key(key)
            if isinstance(value, str):
                new_dict[new_key] = value
                continue
            if isinstance(value, dict):
                # 继续解析dict对象
                new_value = ConvertCamel.deal_with_dict_object(value)
                new_dict[new_key] = new_value
                continue
            if isinstance(value, bool):
                new_dict[new_key] = value
                continue
            if isinstance(value, numbers.Number):
                new_dict[new_key] = value
                continue
        print(json.dumps(new_dict, indent=2))

    @staticmethod
    def deal_with_dict_object(value) -> dict:
        new_dict = dict()
        for key, value in value.items():
            new_key = ConvertCamel.convert_key(key)
            if isinstance(value, str):
                new_dict[new_key] = value
                continue
            if isinstance(value, dict):
                new_value = ConvertCamel.deal_with_dict_object(value)
                new_dict[new_key] = new_value
                continue
            if isinstance(value, bool):
                new_dict[new_key] = value
                continue
            if isinstance(value, list):
                temp_list = list()
                for element in value:
                    temp_list.append(ConvertCamel.deal_with_dict_object(element))
                new_dict[new_key] = temp_list

        return new_dict


if __name__ == '__main__':
    path = sys.argv[1]
    ConvertCamel.cover_camel(path)
