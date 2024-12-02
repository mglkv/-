import json
import os
from graphviz import Digraph
import unittest
import requests

class DependencyVisualizer:
    def __init__(self, config_path):
        # Чтение конфигурации из файла
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.graph_tool_path = config.get("graph_tool_path")
        self.package_name = config.get("package_name")
        self.output_path = config.get("output_path")
        self.repository_url = config.get("repository_url")

    def get_dependencies_from_nuget(self, package_name):
        """
        Получает зависимости из репозитория NuGet для заданного пакета.
        
        :param package_name: Имя пакета .NET
        :return: Список зависимостей
        """
        url = f"https://www.nuget.org/api/v2/Packages(Id='{package_name}')/DependencySets"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            dependencies = []
            for entry in data.get('catalogEntries', []):
                if 'dependencies' in entry:
                    for dep in entry['dependencies']:
                        dependencies.append(dep['id'])
            return dependencies
        else:
            print(f"Error fetching dependencies for package {package_name}")
            return []

    def fetch_dependencies(self, package_name):
        """
        Метод для получения зависимостей пакета .NET.
        
        :param package_name: Имя пакета .NET
        :return: Список зависимостей
        """
        # Вызов функции для получения зависимостей из NuGet
        return self.get_dependencies_from_nuget(package_name)

    def build_dependency_graph(self, package_name, dependencies):
        """
        Строит граф зависимостей в формате Graphviz.
        
        :param package_name: Имя пакета для начала построения графа
        :param dependencies: Список зависимостей пакета
        :return: Исходный код графа в формате DOT
        """
        graph = Digraph(format='dot')
        graph.attr(rankdir="LR")
        
        for dep in dependencies:
            graph.edge(package_name, dep)
        
        return graph.source  # Возвращает исходный код графа, а не сам граф

    def build_full_dependency_graph(self, package_name, graph=None, visited=None):
        """
        Строит полный граф зависимостей, включая транзитивные зависимости.
        
        :param package_name: Имя пакета для начала построения графа
        :param graph: Граф зависимостей (по умолчанию None)
        :param visited: Множество посещенных пакетов (по умолчанию None)
        :return: Граф зависимостей
        """
        if graph is None:
            graph = Digraph(format='dot')
            graph.attr(rankdir="LR")
        if visited is None:
            visited = set()

        if package_name in visited:
            return graph

        visited.add(package_name)
        dependencies = self.fetch_dependencies(package_name)

        for dependency in dependencies:
            graph.edge(package_name, dependency)
            self.build_full_dependency_graph(dependency, graph, visited)

        return graph

    def visualize(self):
        """
        Визуализирует зависимости в виде Graphviz кода и сохраняет его в файл.
        """
        graph = self.build_full_dependency_graph(self.package_name)
        graph_code = graph.source
        print(graph_code)  # Вывод графа в консоль
        with open(self.output_path, 'w') as output_file:
            output_file.write(graph_code)

# Тесты
class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config_path = "config.json"
        self.config_data = {
            "graph_tool_path": "/usr/bin/dot",
            "package_name": "Newtonsoft.Json",
            "output_path": "output.dot",
            "repository_url": "https://api.nuget.org/v3/registration5-gz-semver2"
        }
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config_data, config_file)

        self.visualizer = DependencyVisualizer(self.config_path)

    def tearDown(self):
        os.remove(self.config_path)
        if os.path.exists(self.config_data["output_path"]):
            os.remove(self.config_data["output_path"])

    def test_fetch_dependencies(self):
        expected = ["PackageB", "PackageC"]
        result = self.visualizer.fetch_dependencies("PackageA")
        self.assertEqual(result, expected)

    def test_build_dependency_graph(self):
        dependencies = ["PackageB", "PackageC"]
        graph_code = self.visualizer.build_dependency_graph("PackageA", dependencies)
        self.assertIn('PackageA -> PackageB', graph_code)
        self.assertIn('PackageA -> PackageC', graph_code)

    def test_visualize_creates_output_file(self):
        self.visualizer.visualize()
        self.assertTrue(os.path.exists(self.config_data["output_path"]))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=sys.argv[:1])
    else:
        if len(sys.argv) != 2:
            print("Usage: python script.py <config.json>")
            sys.exit(1)

        config_path = sys.argv[1]
        if not os.path.exists(config_path):
            print(f"Configuration file {config_path} does not exist.")
            sys.exit(1)

        visualizer = DependencyVisualizer(config_path)
        visualizer.visualize()



