import unittest
from unittest.mock import patch, MagicMock

import main 


class TestMCPTools(unittest.TestCase):

    # ----------------------------------
    # system_info_tool
    # ----------------------------------
    @patch("main.system_info.get_system_info")
    def test_system_info_tool(self, mock_get_system_info):

        mock_info_obj = MagicMock()
        mock_info_obj.to_dict.return_value = {
            "System": "Windows",
            "CPU Usage": 30,
            "RAM": 16.0
        }

        mock_get_system_info.return_value = mock_info_obj

        result = main.system_info_tool()

        self.assertEqual(result["System"], "Windows")
        self.assertEqual(result["CPU Usage"], 30)
        mock_get_system_info.assert_called_once()


    # ----------------------------------
    # resource_usage_tool
    # ----------------------------------
    @patch("main.validation.get_safe_to_terminate_process")
    @patch("main.system_info.check_high_resource_usage")
    def test_resource_usage_tool(
        self,
        mock_check_usage,
        mock_validation
    ):

        mock_process = MagicMock()
        mock_process.to_dict.return_value = {"pid": 1234}

        mock_check_usage.return_value = ["raw_process"]
        mock_validation.return_value = [mock_process]

        result = main.resource_usage_tool()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["pid"], 1234)


    # ----------------------------------
    # terminate_process_tool - no confirm
    # ----------------------------------
    def test_terminate_process_without_confirmation(self):

        result = main.terminate_process_tool(
            pid=111,
            confirmed=False
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["pid"], 111)


    # ----------------------------------
    # terminate_process_tool - success
    # ----------------------------------
    @patch("main.system_info.terminate_process_with_validation")
    def test_terminate_process_success(self, mock_terminate):

        mock_terminate.return_value = {"success": True}

        result = main.terminate_process_tool(
            pid=111,
            confirmed=True
        )

        mock_terminate.assert_called_once_with(111)
        self.assertTrue(result["success"])


    # ----------------------------------
    # list_processes_tool
    # ----------------------------------
    @patch("main.system_info.get_processes")
    def test_list_processes_tool(self, mock_get_processes):

        mock_proc = MagicMock()
        mock_proc.to_dict.return_value = {"pid": 1}

        mock_get_processes.return_value = [mock_proc, mock_proc]

        result = main.list_processes_tool(2)

        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["processes"]), 2)
        self.assertEqual(result["processes"][0]["pid"], 1)


if __name__ == "__main__":
    unittest.main()