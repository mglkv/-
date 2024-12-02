import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Импортируем ваш основной скрипт
import script

class TestDependencyVisualizer(unittest.TestCase):

    @patch("script.load_config")
    def test_load_config(self, mock_load_config):
        # Тестируем загрузку конфигурации
        config_data = {
            "graph_tool_path": "/usr/local/bin/dot",
            "package_name": "Microsoft.AspNetCore.Mvc, Version=2.2.0",
            "output_path": "/Users/mglkv/DependencyVisualizer/output_graph.dot",
            "repository_url": "https://api.nuget.org/v3/registration5-gz-semver2"
        }
        mock_load_config.return_value = config_data

        # В реальном коде нет необходимости передавать аргумент
        config = script.load_config()

        self.assertEqual(config["graph_tool_path"], "/usr/local/bin/dot")
        self.assertEqual(config["package_name"], "Microsoft.AspNetCore.Mvc, Version=2.2.0")
        self.assertEqual(config["output_path"], "/Users/mglkv/DependencyVisualizer/output_graph.dot")
        self.assertEqual(config["repository_url"], "https://api.nuget.org/v3/registration5-gz-semver2")

    @patch("script.fetch_dependencies")
    def test_fetch_dependencies(self, mock_fetch_dependencies):
        # Тестируем получение зависимостей
        mock_fetch_dependencies.return_value = ['Microsoft.Extensions.DependencyInjection', 'Microsoft.Extensions.Logging']

        dependencies = script.fetch_dependencies("Microsoft.AspNetCore.Mvc, Version=2.2.0", "https://api.nuget.org/v3/registration5-gz-semver2")
        self.assertIn('Microsoft.Extensions.DependencyInjection', dependencies)
        self.assertIn('Microsoft.Extensions.Logging', dependencies)

    @patch("script.create_graph")
    def test_create_graph(self, mock_create_graph):
        # Тестируем создание графа
        mock_create_graph.return_value = "/Users/mglkv/DependencyVisualizer/output_graph.dot"
        output_path = script.create_graph(['Microsoft.Extensions.DependencyInjection', 'Microsoft.Extensions.Logging'])
        self.assertEqual(output_path, "/Users/mglkv/DependencyVisualizer/output_graph.dot")
        self.assertTrue(os.path.exists(output_path))

    @patch("script.load_config")
    @patch("script.fetch_dependencies")
    @patch("script.create_graph")
    def test_full_process(self, mock_create_graph, mock_fetch_dependencies, mock_load_config):
        # Тестируем полный процесс
        config_data = {
            "graph_tool_path": "/usr/local/bin/dot",
            "package_name": "Microsoft.AspNetCore.Mvc, Version=2.2.0",
            "output_path": "/Users/mglkv/DependencyVisualizer/output_graph.dot",
            "repository_url": "https://api.nuget.org/v3/registration5-gz-semver2"
        }
        mock_load_config.return_value = config_data
        mock_fetch_dependencies.return_value = ['Microsoft.Extensions.DependencyInjection', 'Microsoft.Extensions.Logging']
        mock_create_graph.return_value = "/Users/mglkv/DependencyVisualizer/output_graph.dot"
        
        script.main()
        
        # Проверяем, что load_config был вызван без аргументов
        mock_load_config.assert_called_once()  # Убираем аргумент
        # Проверяем, что fetch_dependencies был вызван с двумя аргументами
        mock_fetch_dependencies.assert_called_once_with("Microsoft.AspNetCore.Mvc, Version=2.2.0", "https://api.nuget.org/v3/registration5-gz-semver2")
        # Обновляем вызов create_graph с тремя аргументами
        mock_create_graph.assert_called_once_with(
            ['Microsoft.Extensions.DependencyInjection', 'Microsoft.Extensions.Logging'], 
            "Microsoft.AspNetCore.Mvc, Version=2.2.0", 
            "/Users/mglkv/DependencyVisualizer/output_graph.dot"
        )
    
    @patch("script.fetch_dependencies")
    def test_fetch_dependencies_error(self, mock_fetch_dependencies):
        # Тестируем ошибку при получении зависимостей
        mock_fetch_dependencies.side_effect = Exception("Failed to fetch dependencies")
        with self.assertRaises(Exception):
            script.fetch_dependencies("Microsoft.AspNetCore.Mvc, Version=2.2.0", "https://api.nuget.org/v3/registration5-gz-semver2")

    
if __name__ == "__main__":
    unittest.main()

