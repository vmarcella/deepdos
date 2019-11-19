import subprocess
import unittest
import unittest.mock as mock

import deepdos.utils.processes as proc


def proc_close_success():
    """
        Successfully closed command
    """
    return 0


def proc_close_fail():
    """
        Failed to close command
    """
    return 1


def stub_pcap_line_data():
    """
        Stub the pcap line data inside of the test
    """
    for value in ["hello", "432432"]:
        yield value


class ProcessTests(unittest.TestCase):
    @mock.patch("deepdos.utils.processes.subprocess.Popen")
    def test_successful_capture_pcap(self, mock_process):
        """
            Test to ensure that pcap succeeds under normal capture
        """
        # Initialize stub functions
        mock_process.return_value.wait = proc_close_success
        mock_process.return_value.stdout.readline = stub_pcap_line_data
        mock_process.return_value.stdout.close.return_value = 0
        output_list = proc.proc_capture_pcap("enp3s0", 2)

        # Assert we get the length of the desired data
        assert len(output_list) == 2

    @mock.patch("deepdos.utils.processes.subprocess.Popen")
    def test_failed_pcap(self, mock_process):
        """
            Test to ensure that pcap fails when process closes
        """
        # Initialize stub functions
        mock_process.return_value.wait = proc_close_fail
        mock_process.return_value.stdout.readline.return_value = stub_pcap_line_data
        mock_process.return_value.stdout.close.return_value = 0

        # Ensure that the subprocess throws an error due to a failed process close
        self.assertRaises(
            subprocess.CalledProcessError, proc.proc_capture_pcap, "enp3s0", 1
        )

    @mock.patch("deepdos.utils.processes.subprocess.Popen")
    def test_successfull_find_deepdos(self, mock_proc):
        """
            Test a successful run for finding deepdos
        """
